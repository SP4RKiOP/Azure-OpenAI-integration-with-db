# Azure-OpenAI-integration-with-db

Welcome to Azure-OpenAI-integration-with-db! This project utilizes [Flask](https://flask.palletsprojects.com/) and [Azure OpenAI](https://azure.microsoft.com/en-us/services/cognitive-services/openai/) to provide an interactive query system.

## Getting Started

These instructions will guide you through setting up and running the project locally.

### Prerequisites

- Azure OPENAI key, base_url etc
- Python 3.8 or higher

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/SP4RKiOP/Azure-OpenAI-integration-with-db.git
   cd your-project
   
2. Install the required packages:
     pip install -r requirements.txt

### Configuration

1. Set your Azure OpenAI API key, base_url, and your deployment name in `utils.py`:

   ```python
   os.environ["OPENAI_API_KEY"] = "change with your key"
   os.environ["OPENAI_API_BASE"] = "change with your base url"
   os.environ["OPENAI_API_VERSION"] = "change with your version"
   deployment_name = "change with your model name"  # (in llm connection string)

2. Set your database connection string:
   
   ```python
   db = SQLDatabase.from_uri("mssql+pymssql://dbServerName:Password@dbServerName.database.windows.net:1433/dbName")

### Usage

1. Start the server using waitress-serve:

   ```bash
   waitress-serve --call wsgi:create_app
  
2. The application will be accessible at http://localhost:8080.

## Contributing

If you'd like to contribute to this project, feel free to do.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
   

   
