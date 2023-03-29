from psycopg2 import connect, Error

#Connection to DataBase Class
class DbConnection:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    #Method for Connection to DataBase
    def connect(self):
        try:
            self.conn = connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()

        except Error as e:
            print(f"Unable to connect to the database: {e}")

    #Method for disconnection to DataBase
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Disconnected from Postgres database")

    #Method for execute for Select All rows
    def execute_query_select_all(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Unable to execute the query: {e}")

    #Method for execute for select one row
    def execute_query_select_one(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Unable to execute the query: {e}")

    
    #Method for DDL operations
    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(f"Unable to execute the query: {e}")