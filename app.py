# from dotenv import load_dotenv
# load_dotenv()

# import streamlit as st
# import os
# import sqlite3
# import google.genai.Model as genai

# # print(os.getenv("GOOGLE_API_KEY"))
# # Configure Gemini API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



# # Function to load Google Gemini Model and Provide SQL query as response
# def get_gemini_response(question, prompt):
#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content([question,prompt[0]])
#     return response.text

# # Function to retrieve query results from the SQL database
# def read_sql_query(sql, db):
#         conn = sqlite3.connect(db)
#         cur = conn.cursor()
#         cur.execute(sql)
#         rows = cur.fetchall()
#         conn.commit()
#         conn.close()
#         for row in rows:
#             print(row)
#         return rows

# # Prompt for Gemini model
# prompt = """
# You are an expert in converting English questions to SQL queries!
# The SQL database has the name STUDENT and has the following columns: NAME, CLASS, SECTION, and MARKS.

# For example:
# 1. "How many records are present?"  
#    SQL: `SELECT COUNT(*) FROM Student;`
# 2. "Tell me all students in the Data Science class?"  
#    SQL: `SELECT * FROM Student WHERE CLASS='Data Science';`

# Please generate SQL queries **without** surrounding triple quotes (`'''`) or extra text.
# """

# # Streamlit app setup
# st.set_page_config(page_title="Text-to-SQL Query App")
# st.header("Convert Natural Language to SQL Queries")

# question = st.text_input("Enter your question:", key="input")
# submit=st.button("Ask the Question")
# if submit:
#     response = get_gemini_response(question, prompt)
#     print(response)
#     data = read_sql_query(response, "student.db")
#     st.subheader("The Response is: ")
#     for row in data:
#         print(row)
#         st.header(row)

    

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide SQL query as response
def get_gemini_response(question, prompt):
    # Use a supported model, e.g., "gemini-1.5-pro-latest"
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content([question, prompt])
    return response.text

# Function to retrieve query results from the SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Prompt for Gemini model
prompt = """
You are an expert in converting English questions to SQL queries!
The SQL database has the name EMPLOYEE and has the following columns: NAME, BRANCH, SECTION, Working_Hours, and Project_Pending.

For example:
1. "How many records are present?"  
   SQL: `SELECT COUNT(*) FROM employee;`
2. "Tell me all employee in the Machine Learning branch?"  
   SQL: `SELECT * FROM employee WHERE BRANCH='Machine Learning';`
3. "Find average working hours of employee?"
    SQL: `Select avg(Working_Hours) from employee;`
4. ""
Please generate SQL queries **without** surrounding triple quotes (`'''`) or extra text.
"""

# Streamlit app setup

st.set_page_config(page_title="Text-to-SQL Query App")

st.image("logo.jpeg",width=300)
st.header("Convert Natural Language to SQL Queries")

question = st.text_input("Enter your question:", key="input")
submit = st.button("Ask the Question")

if submit:
    response = get_gemini_response(question, prompt)
    st.subheader("Generated SQL Query:")
    st.code(response)  # Display the generated SQL query

    # Execute the SQL query and display results
    try:
        data = read_sql_query(response, "EMPLOYEE.db")
        st.subheader("Query Results:")
        for row in data:
            st.write(row)
    except sqlite3.Error as e:
        st.error(f"An error occurred while executing the SQL query: {e}")