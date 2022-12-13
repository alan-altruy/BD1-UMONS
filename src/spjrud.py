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

    @staticmethod
    def join(first_table, second_table):
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

    @staticmethod
    def union(first_table, second_table):
        return first_table + " UNION " + second_table

    @staticmethod
    def diff(first_table: str, second_table: str):
        return first_table + " EXCEPT " + second_table

    def create_expression(self, name: str, expression: str):
        if name not in self.expressions.keys() and name not in self.get_tables():
            sql_request = self.check_expression(expression)

            if type(sql_request) == str:  # is an error
                self.expressions[name] = [expression, sql_request]
                return "Relation successfully added !"
            return sql_request
        else:
            return "An table/relation already has this name !"

    def check_expression(self, expression: str):
        operators = {"sel": self.check_select, "proj": self.check_project, "join": self.check_join,
                     "ren": self.check_rename, "union": self.check_union, "diff": self.check_difference}
        operator = ""
        args = ""
        pointer = "operator"
        if expression.count('(') != expression.count(')'):
            return error_syntax(expression, "parentheses")

        for character in expression:
            if pointer == "operator":
                if character == '(':
                    pointer = "args"
                else:
                    operator += character
            else:
                args += character
        if operator not in operators.keys():
            return error_operator(expression, operator, list(operators.keys()))
        return operators[operator](args[:-1])

    def check_relation(self, relation: str, exp: str):
        if relation.find("(") > 0:
            return self.check_expression(relation)
        elif self.table_exist(relation):
            return "select * from " + relation
        elif self.relation_exist(relation):
            return self.expressions[relation][1]
        else:
            return error_rel_not_exist(exp, relation)

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

        if "" in args:
            return error_arg_miss(expression)

        [first_arg, operator, second_arg, relation] = clean_lst_str(args)

        sql_request = self.check_relation(relation, expression)
        if type(sql_request) == list:
            return sql_request

        cols = self.get_column(sql_request)
        schema = self.get_schema_table(sql_request, cols)

        if is_constant(first_arg):
            return error_column_constant(expression, first_arg)

        if first_arg not in cols:
            return error_column(expression, relation, first_arg, cols)

        if operator not in operators:
            return error_operator(expression, operator, operators)

        if not is_constant(second_arg) and second_arg not in cols:
            return error_column(expression, relation, second_arg, cols)

        if not is_constant(second_arg) and schema[first_arg] != schema[second_arg]:
            return error_type_column(expression, first_arg, second_arg, schema)

        if is_constant(second_arg) and not check_same_type(clean_cons(second_arg), schema[first_arg]):
            return error_type(expression, second_arg, first_arg, schema[first_arg])

        return self.select(first_arg, operator, second_arg, sql_request)

    def check_project(self, arg: str):
        expression = "proj(" + arg + ")"
        arg = clean_str(arg)
        if not arg.startswith("["):
            return error_syntax(expression, "brackets")
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
            return error_syntax(expression, "brackets")
        cols_to_project = clean_lst_str(cols_to_project)
        relation = clean_str(buffer)
        sql_request = self.check_relation(relation, expression)
        if type(sql_request) == list:
            return sql_request

        cols = self.get_column(sql_request)
        for col in cols_to_project:
            if col not in cols:
                return error_column(expression, relation, col, cols)

        return self.proj(cols_to_project, sql_request)

    def check_join(self, arg: str):
        expression = "join(" + arg + ")"
        value = self.check_args_relations(arg, expression)
        if type(value) == list:
            return value
        (rel1, sql_request1, sch1, rel2, sql_request2, sch2) = value
        # TODO

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
        sql_request = self.check_relation(relation, expression)
        if type(sql_request) == list:
            return sql_request

        cols = self.get_column(sql_request)
        if args[0] not in cols:
            return error_column(expression, relation, args[0], cols)
        if not is_constant(args[1]):
            return error_not_constant(expression, args[1])
        if not check_same_type(args[1], 'text'):
            return error_type(expression, args[1], "[New Name]", 'text')
        return self.rename(args[0], args[1], sql_request, cols)

    def check_union(self, arg: str):
        expression = "union(" + arg + ")"
        value = self.check_args_relations(arg, expression)
        if type(value) == list:
            return value
        (rel1, sql_request1, sch1, rel2, sql_request2, sch2) = value
        if sch1 != sch2:
            return error_schema(expression, rel1, sch1, rel2, sch2)
        return self.union(sql_request1, sql_request2)

    def check_difference(self, arg: str):
        expression = "diff(" + arg + ")"
        value = self.check_args_relations(arg, expression)
        if type(value) == list:
            return value
        (rel1, sql_request1, sch1, rel2, sql_request2, sch2) = value
        if sch1 != sch2:
            return error_schema(expression, rel1, sch1, rel2, sch2)
        return self.diff(sql_request1, sql_request2)

    def check_args_relations(self, arg: str, exp: str):
        arg = clean_str(arg)
        nb_opened_par = 0
        nb_closed_par = 0
        rel1 = ""

        for char in arg:
            if char == '(':
                nb_opened_par += 1
            elif char == ')':
                nb_closed_par += 1
            if char == ',' and nb_opened_par == nb_closed_par:
                break
            else:
                rel1 += char
        rel2 = clean_str(arg[len(rel1) + 1:])
        rel1 = clean_str(rel1)

        sql_request1 = self.check_relation(rel1, exp)
        if type(sql_request1) == list:
            return sql_request1

        sql_request2 = self.check_relation(rel2, exp)
        if type(sql_request2) == list:
            return sql_request2
        tab1 = self.get_table_from_query(sql_request1)
        sch1 = self.get_schema_table(sql_request1, tab1[0])

        tab2 = self.get_table_from_query(sql_request2)
        sch2 = self.get_schema_table(sql_request2, tab2[0])

        return rel1, sql_request1, sch1, rel2, sql_request2, sch2

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
        schema = {}
        for i in range(len(datas)):
            schema[cols[i]] = datas[i]
        return schema

    def get_table_relation(self):
        data = self.cursor.fetchall()
        table = []
        col = []
        for elt in self.cursor.description:
            col.append(elt[0])
        table.append(col)
        table.extend(data)
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
