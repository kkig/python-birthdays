import os
import mysql.connector
from mysql.connector import errorcode


# SMQ connector doc:
# https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html


class Config:
    @staticmethod
    def init():
        _config = {
            "user": "root",
            "host": "db",
            "database": "example",
        }

        try:
            pwd = open("/run/secrets/db-password", "r")
            _config["password"] = pwd.read()
            pwd.close()
            return _config
        except ValueError:
            print("Error opening password file.")


class DB:
    def __init__(self):
        self.conn = self._start(Config.init())
        self.cursor = self.conn.cursor()

    def _start(self, config):
        try:
            return mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            exit(1)

    def populate(self):
        tableName = "persons"

        # self.cursor.execute("DROP TABLE IF EXISTS persons")
        # self.cursor.execute("CREATE TABLE persons (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), birthday DATE)")
        try:
            self.cursor.execute(
                f"CREATE TABLE {tableName} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))"
            )
            self.cursor.executemany(
                f"INSERT INTO {tableName} (id, name) VALUES (%s, %s);",
                [(i, "User #%d" % i) for i in range(5)],
            )
            self.connection.commit()
        except:
            print("Error creating table persons.")

    def query_names(self):
        self.cursor.execute("SELECT name FROM persons")
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec
