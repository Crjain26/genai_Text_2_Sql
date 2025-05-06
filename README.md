# Genai_Text_2_Sql
Genai_Text_2_Sql is a Python-based application that translates natural language queries into SQL statements. It provides a user-friendly interface for users to interact with databases using plain English, making data retrieval more accessible.

## Features:

🔍 Text-to-SQL Translation: Enter natural language queries and receive executable SQL.

📊 PostgreSql Database Integration: Queries are executed on a local SQLite database.

🌐 Streamlit UI: Clean and interactive web interface.

🧩 Modular Design: Easily customizable and extendable for other databases or models.


### Clone the Repository

>Bash commands
```
git clone https://github.com/Crjain26/HPE_Text_2_Sql.git

cd genai_Text_2_Sql

```

### Step 1:
>Create a virtual environment in python.

```
python -m venv myvenv

```
### Step 2:
>Activate The enevironment
```
myvenv\Scripts\activate
```

### Step 3:
>Check python and pip version
```
python --version
pip --version
```
Python version should be (3.8.0 - <3.12.0) 

Pip upgrade:
```
python -m pip install --upgrade pip

```

### Step 4:
>Download the required dependencies of project
```
pip install -r requirements.txt
``` 

### Step 5:
>Create a API key from ***https://aistudio.google.com/prompts/new_chat***.

>Click on Get API key.

>Update the GOOGLE_API_KEY in the .env file 

### Step 6:
>Update your credentials of postgreSql.

>Provide database name and password from your pgAdmin.

### Step 7:
>To run the streamlit app
```
streamlit run app.py
```

## Acknowledgements

OpenAI for providing powerful language models.

Streamlit for the interactive web interface.

PostegreSQL for dynamic integration.



## License
This project is licensed under the MIT License.
