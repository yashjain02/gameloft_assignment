import pickle
import snowflake.connector
import pandas as pd

class Snowflake:
    def __init__(self, account: str, user: str, password: str, warehouse: str, database: str, schema: str):
        self.account = account
        self.user = user
        self.password = password
        self.warehouse = warehouse
        self.database = database
        self.schema = schema

    def query(self, text: str) -> pd.DataFrame:
        conn = snowflake.connector.connect(
            account=self.account,
            user=self.user,
            password=self.password,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema
        )

        cursor = conn.cursor()
        cursor.execute(text)
        data = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)

        cursor.close()
        conn.close()

        return df

class SnowflakeQuery:
    def __init__(self, query: str, binary_file_name: str):
        self.query = query
        self.binary_file_name = binary_file_name

    def store(self):
        with open(self.binary_file_name, 'wb') as file:
            pickle.dump(self, file)

def take_user_query():
    file_name = input("Hello, could you please provide the name of the file for your query, the file will be stored on your machine: ")

    if file_name:
        print("Could you please provide the query you want to store the query definition will end with ';'")
        query_lines = []
        while True:
            line = input()
            if line.endswith(';'):
                query_lines.append(line)
                break
            query_lines.append(line)

        query = '\n'.join(query_lines)
        snowflake_query = SnowflakeQuery(query, file_name)
        snowflake_query.store()
        print(f"Thank you, your query has been registered under the file name {file_name}")
    else:
        print("Invalid input. Please provide a file name.")

take_user_query()
