import sqlite3 as sql


class SPJRUD:
    connection: sql.Connection
    cursor: sql.Cursor

    expressions = {}

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

    def create_expression(self, name: str, expression: str):
        if name not in self.expressions.keys() and name not in self.get_tables():
            self.expressions[name] = expression
            return "Relation successfully added !"
        else:
            return "An table/relation already has this name !"
        # TODO check if the expression is possible

    def get_expressions(self):
        return self.expressions

    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = []
        for table in self.cursor.fetchall():
            tables.append(table[0])
        return tables

    def get_table(self, table_name: str):
        self.cursor.execute("SELECT * FROM " + table_name + ";")
        data = self.cursor.fetchall()
        table = []
        col = []
        for elt in self.cursor.description:
            col.append(elt[0])
        table.append(col)
        for elt in data:
            table.append(elt)
        return table

    def table_exist(self, table_name):
        try:
            self.cursor.execute("SELECT * FROM " + table_name + ";")
            return True
        except:
            return False
