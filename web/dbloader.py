import os
import mysql.connector
from mysql.connector import errorcode


# SMQ connector doc:
# https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html


class DB:
    def __init__(self, database="example", host="db", user="root", password_file=None):
        try:
            pwf = open(password_file, "r")
            self.connection = mysql.connector.connect(
                user=user,
                password=pwf.read(),
                host=host, # name of the mysql service as set in the docker compose file
                database=database,
                auth_plugin="mysql_native_password"
            )
            pwf.close()
            self.cursor = self.connection.cursor()

            # self.connection = self._connect(password_file)
            # self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
    

    def populate(self):
        tableName = "persons"
        # datas = [
        #     {
        #     "name": "name", 
        #     "type": "VARCHAR(255))"
        #     },
        #     {
        #         "name": "birthday",
        #         "type": ""
        #      }
        # ]
        # self.cursor.execute("DROP TABLE IF EXISTS persons")
        # self.cursor.execute("CREATE TABLE persons (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), birthday DATE)")
        try:
            self.cursor.execute(f"CREATE TABLE {tableName} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
            self.cursor.executemany(f"INSERT INTO {tableName} (id, name) VALUES (%s, %s);", [(i, "User #%d"% i) for i in range(5)])
            self.connection.commit()
        except:
            print("Error creating table persons.")



    def query_names(self):
        self.cursor.execute("SELECT name FROM persons")
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec