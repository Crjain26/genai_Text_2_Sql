import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PostgreSQLManager:
    def __init__(self):
        self.connection = None
        self.DB_NAME = os.getenv("POSTGRES_DB", "classicmodels")
        self.DB_USER = os.getenv("POSTGRES_USER", "postgres")
        self.DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Chotu@2603")
        self.DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
        self.DB_PORT = os.getenv("POSTGRES_PORT", "5432")

    def connect(self):
        """Create a database connection to PostgreSQL with collation fix"""
        try:
            self.connection = psycopg2.connect(
                dbname=self.DB_NAME,
                user=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT
            )
            
            # Handle collation version mismatch
            with self.connection.cursor() as cursor:
                try:
                    cursor.execute("ALTER DATABASE %s REFRESH COLLATION VERSION;", 
                                (sql.Identifier(self.DB_NAME),))
                    self.connection.commit()
                except psycopg2.Error as e:
                    print(f"Collation refresh note: {e}")
                    self.connection.rollback()
            
            return self.connection
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            return None

    def get_table_names(self):
        """Get list of tables in the database"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE';
                """)
                return [table[0] for table in cursor.fetchall()]
        except psycopg2.Error as e:
            print(f"Error getting table names: {e}")
            return []

    def get_table_schema(self, table_name):
        """Get schema for a specific table"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = %s;
                """, (table_name,))
                return {column[0]: column[1] for column in cursor.fetchall()}
        except psycopg2.Error as e:
            print(f"Error getting table schema: {e}")
            return {}

    def get_sample_data(self, table_name, limit=3):
        """Get sample rows from a table"""
        try:
            with self.connection.cursor() as cursor:
                query = sql.SQL("SELECT * FROM {} LIMIT {}").format(
                    sql.Identifier(table_name),
                    sql.Literal(limit)
                )
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except psycopg2.Error as e:
            print(f"Error getting sample data: {e}")
            return []

    def execute_query(self, query):
        """Execute a custom SQL query safely"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                
                if cursor.description:  # If it's a SELECT query
                    columns = [desc[0] for desc in cursor.description]
                    records = cursor.fetchall()
                    return columns, records
                else:  # For non-SELECT queries
                    self.connection.commit()
                    return None, None
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return None, None

    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed")
