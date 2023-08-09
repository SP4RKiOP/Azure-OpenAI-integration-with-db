import os, openai, timeout_decorator
from langchain.llms import AzureOpenAI
from langchain.sql_database import SQLDatabase

# class AzureOpenAIWithTimeout(AzureOpenAI):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     @timeout_decorator.timeout(15)  # Set a timeout of 15 seconds (adjust as needed)
#     def generate_with_timeout(self, prompt, max_tokens, stop=None):
#         return self.generate(prompt, max_tokens, stop)

def create_llm_object():
    openai.api_type = "azure"
    os.environ["OPENAI_API_KEY"] = "change with your key"
    os.environ["OPENAI_API_BASE"] = "change with your base url"
    os.environ["OPENAI_API_VERSION"] = "change with your version"
    llm =  AzureOpenAI(temperature=0, deployment_name="change with your model name", model_name="text-davinci-003")
    # llm =  AzureOpenAIWithTimeout(temperature=0, deployment_name="change with your model name", model_name="text-davinci-003")
    return llm

def create_db_object():
    db = SQLDatabase.from_uri("mssql+pymssql://dbServerName:Password@dbServerName.database.windows.net:1433/dbName")
    return db