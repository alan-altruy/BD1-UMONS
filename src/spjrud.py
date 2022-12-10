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

    @staticmethod
    def select(first_arg, operation, second_arg, table: str):
        return "select * from (" + table + ") where " + first_arg + " " + operation + " " + second_arg

    @staticmethod
    def proj(columns: list, table: str):
        cols = ""
        for col in columns:
            cols += col + ", "
        return "select " + cols[:-2] + " from (" + table + ")"

    def join(self, first_table, second_table):
        pass

    @staticmethod
    def rename(name_before: str, name_after: str, table, columns: list):
        cols = ""
        for i in range(len(columns)):
            cols += columns[i]
            if columns[i] == name_before:
                cols += " as " + name_after
            cols += ", "
        return "select " + cols[:-2] + " from (" + table + ")"

    def union(self, first_table, second_table):
        pass

    def diff(self, first_table, second_table):
        pass

    def create_expression(self, name: str, expression: str):
        if name not in self.expressions.keys() and name not in self.get_tables():
            error, sql_request = self.check_expression(expression)

            if error is None:
                self.expressions[name] = [expression, sql_request]
                return "Relation successfully added !"
            return error
        else:
            return "An table/relation already has this name !"

    def check_expression(self, expression: str):
        operators = {"sel": self.check_select, "proj": self.check_project, "join": self.check_join,
                     "ren": self.check_rename, "union": self.check_union, "diff": self.check_difference}
        operator = ""
        args = ""
        pointer = "operator"
        if expression.count('(') != expression.count(')'):
            return error_syntax(expression, "parentheses"), None

        for character in expression:
            if pointer == "operator":
                if character == '(':
                    pointer = "args"
                else:
                    operator += character
            else:
                args += character
        if operator not in operators.keys():
            return error_operator(operator, expression, list(operators.keys())), None
        return operators[operator](args[:-1])

    def check_relation(self, relation: str, exp: str):
        if relation.find("(") > 0:
            return self.check_expression(relation)
        elif self.table_exist(relation):
            return None, "select * from " + relation
        elif self.relation_exist(relation):
            return None, self.expressions[relation][1]
        else:
            return error_rel_not_exist(relation, exp), None

    def check_select(self, arg: str):
        expression = "sel(" + arg + ")"
        operators = ["<", ">", "="]
        args = ["", "", "", ""]
        pointer = 0
        for char in arg:
            if (char == ",") and (pointer < 3):
                pointer += 1
            else:
                args[pointer] = args[pointer] + char

        [first_arg, operator, second_arg, relation] = clean_lst_str(args)

        if operator not in operators:
            return error_operator(operator, expression, operators), None

        (error, sql_request) = self.check_relation(relation, expression)
        if error is not None:
            return error, None

        cols = self.get_column(sql_request)

        if is_constant(first_arg):
            return error_column(relation, cols), None

        if first_arg not in cols:
            return error_column(relation, cols, col=first_arg), None

        if not is_constant(second_arg) and second_arg not in cols:
            return error_column(relation, cols, col=second_arg), None

        return None, self.select(first_arg, operator, second_arg, sql_request)

    def check_project(self, arg: str):
        expression = "proj(" + arg + ")"
        arg = clean_str(arg)
        if not arg.startswith("["):
            return error_syntax(expression, "brackets"), None
        arg = arg[1:]
        pointer = "cols"
        cols_to_project = []
        buffer = ""
        for char in arg:
            if char == "," and pointer == "cols":
                cols_to_project.append(buffer)
                buffer = ""
            elif char == "]":
                cols_to_project.append(buffer)
                pointer = "relation"
                buffer = ""
            elif not (buffer == "" and char == ","):
                buffer += char
        if pointer == "cols":
            return error_syntax(expression, "brackets"), None
        cols_to_project = clean_lst_str(cols_to_project)
        relation = clean_str(buffer)
        (error, sql_request) = self.check_relation(relation, expression)
        if error is not None:
            return error, None

        cols = self.get_column(sql_request)
        for col in cols_to_project:
            if col not in cols:
                return error_column(relation, cols, col=col), None

        return None, self.proj(cols_to_project, sql_request)

    def check_join(self, args: str):
        pass

    def check_rename(self, arg: str):
        expression = "ren(" + arg + ")"
        arg = clean_str(arg)
        args = []
        buffer = ""
        for char in arg:
            if char == "," and len(args) < 3:
                args.append(buffer)
                buffer = ""
            else:
                buffer += char
        relation = clean_str(buffer)
        args = clean_lst_str(args)
        (error, sql_request) = self.check_relation(relation, expression)
        if error is not None:
            return error, None

        cols = self.get_column(sql_request)
        if args[0] not in cols:
            return error_column(relation, cols, col=args[0]), None
        if not is_constant(args[1]):
            return error_not_constant(expression, args[1]), None
        return None, self.rename(args[0], args[1], sql_request, cols)

    def check_union(self, args: str):
        pass

    def check_difference(self, args: str):
        pass

    def get_column(self, sql_request: str):
        self.cursor.execute(sql_request)
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

    def get_table_from_query(self, query: str):
        self.cursor.execute(query)
        return self.get_table_relation()

    def get_schema_table(self, sql_request: str, cols: list):
        buffer = "select "
        for col in cols:
            buffer += "typeof(" + col + "), "
        buffer = buffer[:-2] + " from (" + sql_request + ") LIMIT 1"
        self.cursor.execute(buffer)
        datas = list(self.cursor.fetchall()[0])
        schema = []
        for i in range(len(datas)):
            schema.append((cols[i], datas[i]))
        return schema

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

    def is_sql_query(self, query: str):
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            if len(data) == 0:
                return False
            return True
        except:
            return False
