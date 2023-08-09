from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from langchain.agents import *
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor, AgentType, AgentOutputParser
from langchain.prompts.prompt import PromptTemplate
from sqlalchemy.engine import URL
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
#from langchain.tools.sql_database.tool import InfoSQLDatabaseTool, ListSQLDatabaseTool, QueryCheckerTool, QuerySQLDataBaseTool

app = Flask(__name__)
CORS(app)

from utils import create_llm_object, create_db_object
llm = create_llm_object()
db = create_db_object()

# _DEFAULT_TEMPLATE =  """Given an input question, first check table names of database then look into best suitable tables for there column names. 
# Then create a syntactically correct {sql} query to run, then look at the results of the query and return the answer.
# Use the following format:

# Question: "Question here"
# SQLQuery: "SQL Query to run"
# SQLResult: "Result of the SQLQuery"
# Answer: "Final answer here"
# Question:
# {table_info}
#  {input}"""

# PROMPT = PromptTemplate(
#     input_variables=["input", "table_info", "sql"], template=_DEFAULT_TEMPLATE
# )

class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            llm_output = llm_output.split("Question:", 1)[0]
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.strip()},
                log=llm_output,
            )#prints both Thought and Final Answer.
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: {repr(llm_output)}")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

output_parser = CustomOutputParser()

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# assign your llm and db

# info_sql_database_tool_description = """Input to this tool is a comma separated list of tables, output is the schema and sample rows for those tables.Be sure that the tables actually exist by calling list_tables_sql_db first! Example Input: table1, table2, table3"""

# toolkit = [
# QuerySQLDataBaseTool(db=db),
# InfoSQLDatabaseTool(db=db, description=info_sql_database_tool_description),
# ListSQLDatabaseTool(db=db),
# QueryCheckerTool(db=db, llm=llm),
# ]
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    top_k=25,
    output_parser=output_parser
)

@app.route('/api/question', methods=['POST'])
def process_question_with_timeout():
    try:
        data = request.get_json()
        user_input = data['question']
        with ThreadPoolExecutor() as executor:
            future = executor.submit(agent.run, user_input)
            try:
                result = future.result(timeout=30)  # Set a timeout of 14 seconds (adjust as needed)
            except FutureTimeoutError:
                return jsonify({'result': "Timeout. The agent_executor is taking too long to generate the final answer."}), 500

        return jsonify({'result': result})
    except OutputParserException as e:
        return jsonify({'result': str(e)}), 500
    except Exception as e:
        return jsonify({'result': str(e)}), 500

