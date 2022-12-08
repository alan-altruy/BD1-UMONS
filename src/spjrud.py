import sqlite3 as sql
from tools import *


class SPJRUD:
    connection: sql.Connection
    cursor: sql.Cursor

    expressions = {}

    def config(self, database_file: str):
        self.connection = sql.connect(database_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT name FROM sqlite_master;")

    def select(self, first_arg, operation, second_arg, table: str):
        return "select * from (" + table + ") where " + first_arg + " " + operation + " " + second_arg

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
            check, sql = self.check_expression(expression)
            if check is None:
                self.expressions[name] = [expression, sql]
                return "Relation successfully added !"
            return check
        else:
            return "An table/relation already has this name !"

    def check_expression(self, expression: str):
        operators = {"sel": self.check_select, "proj": self.check_project, "join": self.check_join,
                     "ren": self.check_rename, "union": self.check_union, "diff": self.check_difference}
        operator = ""
        args = ""
        pointer = "operator"
        if expression.count('(') != expression.count(')'):
            return ["Syntax error",
                    "One of the parentheses is missing in the (sub-)expression",
                    "   " + expression], None

        for character in expression:
            if pointer == "operator":
                if character == '(':
                    pointer = "args"
                else:
                    operator += character
            else:
                args += character
        if operator not in operators.keys():
            return ["'" + operator + "' in the (sub-)expression:",
                    "   " + expression,
                    "is not an operator",
                    "Here is the list of operators:",
                    "   " + str(operators.keys())[10:-1]], None
        return operators[operator](args[:-1])

    def check_select(self, arg: str):
        operators = ["<", ">", "="]
        args = ["", "", "", ""]
        pointer = 0
        for char in arg:
            if (char == ",") and (pointer < 3):
                pointer += 1
            else:
                args[pointer] = args[pointer] + char
        [first_arg, operator, second_arg, relation] = clean_lst_str(args)
        if relation.find("(") > 0:
            (error, sql) = self.check_expression(relation)
            if error is not None:
                return error, None
        elif self.table_exist(relation):
            sql = "select * from " + relation
        elif self.relation_exist(relation):
            sql = self.expressions[relation][1]
        else:
            return ["The relation '" + relation + "' in the (sub-)expression",
                    "   sel(" + arg + ")",
                    "does not exist"], None
        cols = self.get_column(sql)
        if is_constant(first_arg):
            return ["The first argument must be a column not a constant",
                    "Here is the list of column for the (sub-)expression",
                    "   " + relation + ":",
                    "   " + str(cols)], None

        if first_arg not in cols:
            return ["The column '" + first_arg + "' is not  present in the (sub-)expression",
                    "   " + relation,
                    "which contains the columns:",
                    "   " + str(cols)], None
        if not is_constant(second_arg) and second_arg not in cols:
            return ["The column '" + second_arg + "' is not  present in the (sub-)expression",
                    "   " + relation,
                    "which contains the columns:",
                    "   " + str(cols)], None
        if operator not in operators:
            return "The operator '" + operator + "' does not exist", None

        return None, self.select(first_arg, operator, second_arg, sql)

    def check_project(self, args: str):
        pass

    def check_join(self, args: str):
        pass

    def check_rename(self, args: str):
        pass

    def check_union(self, args: str):
        pass

    def check_difference(self, args: str):
        pass

    def get_column(self, relation: str):
        self.cursor.execute(relation)
        col = []
        for elt in self.cursor.description:
            col.append(elt[0])
        return col

    def get_expressions(self):
        return self.expressions

    def get_relations(self):
        return self.expressions.keys()

    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = []
        for table in self.cursor.fetchall():
            tables.append(table[0])
        return tables

    def get_table(self, table_name: str):
        self.cursor.execute("SELECT * FROM " + table_name)
        return self.get_table_relation()

    def get_table_relation(self):
        data = self.cursor.fetchall()
        table = []
        col = []
        for elt in self.cursor.description:
            col.append(elt[0])
        table.append(col)
        for elt in data:
            table.append(elt)
        return table

    def get_relation(self, table_name):
        self.cursor.execute(self.expressions[table_name][1])
        return self.get_table_relation()

    def table_exist(self, table_name):
        if table_name in self.get_tables():
            return True
        return False

    def relation_exist(self, table_name):
        if table_name in self.expressions:
            return True
        return False
