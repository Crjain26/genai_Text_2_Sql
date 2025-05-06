from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
import pandas as pd
import re
from sql import PostgreSQLManager  # Import the updated PostgreSQLManager

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_dynamic_prompt(table_info, sample_data):
    """Generate prompt based on existing database schema"""
    prompt = """
You are an expert SQL developer with 99% accuracy in converting natural language to PostgreSQL queries.
The database has the following tables with their columns:

"""
    for table_name, schema in table_info.items():
        prompt += f"Table: {table_name}\nColumns:\n"
        for col_name, col_type in schema.items():
            prompt += f"- {col_name} ({col_type})\n"
        
        prompt += "\nSample Data (first 3 rows):\n"
        for row in sample_data.get(table_name, []):
            prompt += str(row) + "\n"
        prompt += "\n"
    
    prompt += """
Rules for SQL Generation:
1. Use exact table and column names as shown
2. Only generate SELECT queries (no INSERT, UPDATE, DELETE, etc.)
3. For string comparisons, use single quotes
4. For dates, use PostgreSQL date functions
5. Use proper JOIN syntax with ON clauses
6. Include all non-aggregated columns in GROUP BY
7. Use CTEs (WITH clauses) for complex queries
8. Handle NULL values properly

Only return the SQL query, no explanations.
"""
    return prompt

def validate_sql(sql_query):
    """Validate SQL query for safety"""
    forbidden = [
        r"(DROP|TRUNCATE)\s+TABLE",
        r"ALTER\s+TABLE",
        r"CREATE\s+(TABLE|DATABASE)",
        r"INSERT\s+INTO",
        r"UPDATE\s+\w+\s+SET",
        r"DELETE\s+FROM",
        r";\s*--",
        r"COPY\s+\w+\s+FROM",
        r"\bpg_\w+\b"
    ]
    return not any(re.search(pattern, sql_query, re.I) for pattern in forbidden)

def main():
    st.set_page_config(page_title="PostgreSQL SQL Generator", layout="wide")
    st.image("logo.jpeg",width=300)
    st.title("Natural Language to PostgreSQL Query Converter")
    
    # Initialize database connection
    db_manager = PostgreSQLManager()
    if not db_manager.connect():
        st.error("Failed to connect to database")
        return
    
    # Add connection form in sidebar
    with st.sidebar:
        st.header("PostgreSQL Connection")
        pg_host = st.text_input("Host", value=db_manager.DB_HOST)
        pg_db = st.text_input("Database", value=db_manager.DB_NAME)
        pg_user = st.text_input("Username", value=db_manager.DB_USER)
        pg_password = st.text_input("Password", type="password", value=db_manager.DB_PASSWORD)
        pg_port = st.text_input("Port", value=db_manager.DB_PORT)
        
        if st.button("Reconnect to Database"):
            db_manager.DB_HOST = pg_host
            db_manager.DB_NAME = pg_db
            db_manager.DB_USER = pg_user
            db_manager.DB_PASSWORD = pg_password
            db_manager.DB_PORT = pg_port
            
            if db_manager.connect():
                st.success("Reconnected successfully!")
            else:
                st.error("Reconnection failed")
    
    try:
        # Get database schema
        table_names = db_manager.get_table_names()
        if not table_names:
            st.warning("No tables found in the database")
            return
            
        table_info = {table: db_manager.get_table_schema(table) for table in table_names}
        sample_data = {table: db_manager.get_sample_data(table) for table in table_names}
        
        # Show database schema
        with st.expander("Database Schema"):
            selected_table = st.selectbox("Select table to view", table_names)
            if selected_table:
                st.subheader(f"Table: {selected_table}")
                st.write(pd.DataFrame.from_dict(table_info[selected_table], orient='index', columns=['Data Type']))
                st.subheader("Sample Data")
                st.dataframe(sample_data[selected_table])
        
        # Generate dynamic prompt
        prompt = generate_dynamic_prompt(table_info, sample_data)
        
        # Query input
        question = st.text_area("Enter your question in natural language:", height=100)
        
        if st.button("Generate SQL"):
            if not question:
                st.warning("Please enter a question")
                return
                
            with st.spinner("Generating PostgreSQL query..."):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash-latest")
                    response = model.generate_content([question, prompt])
                    sql_query = response.text.strip()
                    
                    # Clean up the SQL query
                    sql_query = re.sub(r'^```sql|```$', '', sql_query, flags=re.IGNORECASE).strip()
                    
                    st.subheader("Generated PostgreSQL Query")
                    st.code(sql_query, language="sql")
                    
                    # Validate SQL
                    if not validate_sql(sql_query):
                        st.error("Query validation failed - potentially unsafe operation")
                        return
                    
                    # Execute and show results
                    st.subheader("Query Results")
                    columns, records = db_manager.execute_query(sql_query)
                    if columns and records:
                        df = pd.DataFrame(records, columns=columns)
                        st.dataframe(df)
                    else:
                        st.info("Query executed successfully (no results to display)")
                        
                except Exception as e:
                    st.error(f"Error generating SQL: {str(e)}")
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
    finally:
        db_manager.close()

if __name__ == "__main__":
    main()
