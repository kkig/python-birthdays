import os
import mysql.connector
from mysql.connector import errorcode
from datetime import date


# SMQ connector doc:
# https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html


class Config:
    @staticmethod
    def init():
        _config = {
            "user": "root",
            "host": "db",
            "database": "bdays",
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
        self.config = Config.init()
        self.conn = self._start(self.config)
        self.cursor = self.conn.cursor()
        self._TABALE_NAME = "persons"

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
        # tableName = "persons"

        self.cursor.execute("DROP TABLE IF EXISTS persons")
        self.cursor.execute(
            "CREATE TABLE persons (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, date DATE)"
        )
        try:
            # self.cursor.execute(
            #     f"CREATE TABLE {tableName} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), date DATE)"
            # )
            # self.cursor.executemany(
            #     f"INSERT INTO {tableName} (id, name, date) VALUES (%s, %s, %s);",
            #     [(i, "User #%d" % i, "2009-02-19") for i in range(5)],
            # )
            # self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Blog post #%d'% i) for i in range (1,5)])
            self.cursor.executemany(
                "INSERT INTO persons (name, date) VALUES (%s, %s);",
                [
                    ("Jane", date(2005, 2, 12)),
                    ("Joe", date(2006, 5, 23)),
                    ("John", date(2010, 10, 3)),
                ],
            )
            self.connection.commit()
        except:
            print("Error creating table persons.")

    def query_all(self):
        self.cursor.execute(f"SELECT * FROM {self._TABALE_NAME}")
        rec = []
        for c in self.cursor:
            rec.append(c)
        return rec
