import sqlite3 as sql
import os
from time import sleep


class SJRUD:
    connection: sql.Connection
    cursor: sql.Cursor

    def config(self, database_file: str):
        self.connection = sql.connect(database_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT name FROM sqlite_master;")

    def select(self, column: str, operation, const, table: str):
        self.cursor.execute("select * from" + table + "where " + column + " " + operation + " " + const)
        return self.cursor.fetchall()

    def proj(self, columns: list, table):
        pass

    def join(self, first_table, second_table):
        pass

    def rename(self, name_before: str, name_after: str, table):
        pass

    def union(self, first_table, second_table):
        pass

    def diff(self, first_table, second_table):
        pass

    def show_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("List of tables\n"
              "--------------\n")
        for table in self.cursor.fetchall():
            print(table[0])

    def show_table(self, table_name: str):
        try:
            data = self.cursor.execute("SELECT * FROM "+table_name+";")
            table = self.cursor.fetchall()
            #TODO
            for elt in table:
                print(elt)
            input("\nPress any key to continue..")
        except Exception as e:
            os.system('clear')
            print(e)
            print("! No table has this name !")
            input("\nPress any key to continue..")
            sleep(1)

