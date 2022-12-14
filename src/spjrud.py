import sqlite3 as sql
from tools import *


class SPJRUD:
    connection: sql.Connection
    cursor: sql.Cursor

    relations = {}

    def config(self, database_file: str):
        """
        It connects to a database file, creates a cursor, and then executes a query to get the names of all the tables
        in the database.

        :param database_file: The path to the database file
        :type database_file: str
        """
        self.connection = sql.connect(database_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT name FROM sqlite_master;")

    @staticmethod
    def select(first_arg: str, operator: str, second_arg: str, table: str):
        """
        The above code is creating a SQL query that will select all rows from a table where the first argument is equal
        to the second argument.

        :param first_arg: the first argument in the where clause
        :type first_arg: str
        :param operator: the operator to use in the where clause
        :type operator: str
        :param second_arg: the value you want to compare to
        :type second_arg: str
        :param table: the name of the table you want to select from
        :type table: str
        :return: A string that is a SQL query.
        """
        return "select * from (" + table + ") where " + first_arg + " " + operator + " " + second_arg

    @staticmethod
    def proj(columns: list, table: str):
        """
        It takes a list of columns and a table name, and returns a string that is a SQL query that selects the columns
        from the table

        :param columns: a list of columns to project
        :type columns: list
        :param table: the table you want to select from
        :type table: str
        :return: A string that is a SQL query that selects the columns in the list columns from the table.
        """
        cols = ""
        for col in columns:
            cols += col + ", "
        return "select " + cols[:-2] + " from (" + table + ")"

    def join(self, first_table: str, second_table: str, cols: list):
        """
        It takes two tables and a list of columns, and returns the result of a join on those tables using the columns
        in the list

        :param first_table: the first table to join
        :type first_table: str
        :param second_table: the table you want to join with the first table
        :type second_table: str
        :param cols: list of columns to be selected
        :type cols: list
        :return: The result of the join operation.
        """
        request = "select * from (" + first_table + ") as first, (" + second_table + ") as second where "
        if len(cols) == 0:
            return request + "0 = 1"  # return void table
        for col in cols:
            request += "first." + col + " = second." + col + " and "
        cols = []
        for col in self.get_column(request[:-5]):
            if col not in cols:
                cols.append(col)
        return self.proj(cols, request[:-5])

    @staticmethod
    def rename(name_before: str, name_after: str, table, columns: list):
        """
        It takes a table, a list of columns, and a column name, and returns a new table with the column renamed

        :param name_before: the name of the column you want to rename
        :type name_before: str
        :param name_after: the name you want to rename the column to
        :type name_after: str
        :param table: the table you want to rename the column in
        :param columns: a list of the columns in the table
        :type columns: list
        :return: A string that is a query that renames a column in a table.
        """
        cols = ""
        for i in range(len(columns)):
            cols += columns[i]
            if columns[i] == name_before:
                cols += " as " + name_after
            cols += ", "
        return "select " + cols[:-2] + " from (" + table + ")"

    @staticmethod
    def union(first_table: str, second_table: str):
        """
        This function takes two tables and returns the union of the two tables.

        :param first_table: The first table to be unioned
        :type first_table: str
        :param second_table: The second table to be unioned
        :type second_table: str
        :return: The first table and the second table are being returned unioned.
        """
        return first_table + " UNION " + second_table

    @staticmethod
    def diff(first_table: str, second_table: str):
        """
        This function takes two tables and returns the difference of the two tables.

        :param first_table: The first table to compare
        :type first_table: str
        :param second_table: The table that you want to compare the first table to
        :type second_table: str
        :return: The first table is being returned.
        """
        return first_table + " EXCEPT " + second_table

    def create_expression(self, name: str, expression: str):
        """
        It creates a relation from an expression

        :param name: the name of the relation
        :type name: str
        :param expression: the expression to be checked
        :type expression: str
        :return: An error/validation.
        """
        if name not in self.relations.keys() and name not in self.get_tables_names():
            sql_request = self.check_expression(expression)

            if type(sql_request) == str:  # is an error
                self.relations[name] = [expression, sql_request]
                return "Relation successfully added !"
            return sql_request
        else:
            return "An table/relation already has this name !"

    def check_expression(self, expression: str):
        """
        It takes an expression, checks if it has the right number of parentheses, then checks if the operator is valid,
        and if it is, it calls the appropriate function to check the arguments

        :param expression: the expression to be checked
        :type expression: str
        :return: the result of the function that is called.
        """
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
        """
        If the relation is a subquery, check the subquery. If the relation is a table, return a select statement. If the
        relation is a relation, return the relation's query. Otherwise, return an error

        :param relation: the name of the relation
        :type relation: str
        :param exp: the expression to be checked
        :type exp: str
        :return: The return value is a string.
        """
        if relation.find("(") > 0:
            return self.check_expression(relation)
        elif self.table_exist(relation):
            return "select * from " + relation
        elif self.relation_exist(relation):
            return self.relations[relation][1]
        else:
            return error_rel_not_exist(exp, relation)

    def check_select(self, arg: str):
        """
        It checks if the arguments of the select function are valid, and if they are, it returns the result of the
        select function

        :param arg: the argument of the select function
        :type arg: str
        :return: Table or error
        """
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
        """
        It takes a string as an argument, checks if it's a valid projection, and returns the result of the projection

        :param arg: the string that is passed to the function
        :type arg: str
        :return: Table or error
        """
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
        """
        It takes two relations and returns the join of the two relations

        :param arg: The argument of the function
        :type arg: str
        :return: The join of the two relations.
        """
        expression = "join(" + arg + ")"
        value = self.check_args_two_relations(arg, expression)
        if type(value) == list:  # Is an error
            return value  # The error
        (rel1, sql_request1, sch1, rel2, sql_request2, sch2) = value
        cols1 = self.get_column(sql_request1)
        cols2 = self.get_column(sql_request2)
        cols = []
        for col in cols1:
            if col in cols2:
                cols.append(col)
        return self.join(sql_request1, sql_request2, cols)

    def check_rename(self, arg: str):
        """
        It checks if the rename function is valid, and if it is, it returns the result of the rename function

        :param arg: the argument of the function
        :type arg: str
        :return: Table or error
        """
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
        """
        It checks if the arguments of the union function are valid, and if they are, it returns the union of the two
        relations

        :param arg: the argument passed to the function
        :type arg: str
        :return: The union of the two relations.
        """
        expression = "union(" + arg + ")"
        value = self.check_args_two_relations(arg, expression)
        if type(value) == list:  # Is an error
            return value  # The error
        (rel1, sql_request1, sch1, rel2, sql_request2, sch2) = value
        if sch1 != sch2:
            return error_schema(expression, rel1, sch1, rel2, sch2)
        return self.union(sql_request1, sql_request2)

    def check_difference(self, arg: str):
        """
        It checks if the arguments of the diff function are valid, and if they are, it returns the result of the diff
        function

        :param arg: the argument of the function
        :type arg: str
        :return: The difference between two relations.
        """
        expression = "diff(" + arg + ")"
        value = self.check_args_two_relations(arg, expression)
        if type(value) == list:  # Is an error
            return value  # The error
        (rel1, sql_request1, sch1, rel2, sql_request2, sch2) = value
        if sch1 != sch2:
            return error_schema(expression, rel1, sch1, rel2, sch2)
        return self.diff(sql_request1, sql_request2)

    def check_args_two_relations(self, arg: str, exp: str):
        """
        It takes arguments and expression SPJRUD, and checks if the arguments are two relations and return data for the
        two relations or an error

        :param arg: the argument of the function
        :type arg: str
        :param exp: the expression we're working on
        :type exp: str
        :return: the relation name, the SQL request, the schema of the first table, and the relation name, the SQL
        request and the schema of the second table.
        """
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

    def save_relation_into_db(self, rel_name: str):
        """
        It creates a table in the database with the name of the relation, and then inserts the data from the relation
        into the table

        :param rel_name: the name of the relation to be saved
        :type rel_name: str
        :return: Validation or error message
        """
        if rel_name not in self.relations.keys():
            return "No relation has this name: " + rel_name
        table = self.get_relation(rel_name)
        cols = table[0]
        table = table[1:]
        schema = self.get_schema_table(self.relations[rel_name][1], cols)
        self.relations.pop(rel_name)
        sql_request = "create table " + rel_name + " ("
        for key in schema.keys():
            sql_request += ("'" + key + "' " + schema[key] + ", ")
        sql_request = sql_request[:-2] + ")"
        self.cursor.execute(sql_request)

        for line in table:
            self.cursor.execute("INSERT INTO " + rel_name + " (" + str(cols)[1:-1] + ")VALUES(" + str(line)[1:-1] + ")")
        self.cursor.execute("commit")
        return "Relation successfully saved in database !"

    def get_tables_names(self):
        """
        It returns a list of all the tables in the database
        :return: A list of all the tables in the database.
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = []
        for table in self.cursor.fetchall():
            tables.append(table[0])
        return tables

    def get_relations_names(self):
        """
        It returns a list of the names of the relations in the database
        :return: The keys of the relations dictionary.
        """
        return self.relations.keys()

    def get_relations(self):
        """
        It returns the list of relations that are stored in the object
        :return: The relations are being returned.
        """
        return self.relations

    def get_table(self, table_name: str):
        """
        It returns a table relation from the database

        :param table_name: The name of the table you want to get
        :type table_name: str
        :return: The table relation is being returned.
        """
        return self.get_table_from_query("SELECT * FROM " + table_name)

    def get_relation(self, rel_name):
        """
        It takes a relation name as input and returns a table object that is the result of executing the query that
        defines the relation

        :param rel_name: The name of the relation you want to get
        :return: The table that is being returned is the table that is being queried.
        """
        return self.get_table_from_query(self.relations[rel_name][1])

    def get_table_from_query(self, query: str):
        """
        It takes a query as a string, executes it, and returns the result as a table

        :param query: The query to be executed
        :type query: str
        :return: A table relation
        """
        self.cursor.execute(query)
        return self.get_table_relation()

    def get_table_relation(self):
        """
        It takes the data from the cursor and puts it into a list of lists
        :return: A list of lists.
        """
        data = self.cursor.fetchall()
        table = []
        col = []
        for elt in self.cursor.description:
            col.append(elt[0])
        table.append(col)
        table.extend(data)
        return table

    def get_column(self, sql_request: str):
        """
        It returns the column names of a table

        :param sql_request: the SQL request to be executed
        :type sql_request: str
        :return: The column names of the table.
        """
        self.cursor.execute(sql_request)
        col = []
        for elt in self.cursor.description:
            col.append(elt[0])
        return col

    def get_schema_table(self, sql_request: str, cols: list):
        """
        It takes a SQL request and a list of columns, and returns a dictionary with the columns as keys and the types as
        values

        :param sql_request: the SQL request to be executed
        :type sql_request: str
        :param cols: list of columns to be returned
        :type cols: list
        :return: A dictionary with the column names as keys and the data types as values.
        """
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

    def table_exist(self, table_name):
        """
        If the table name is in the list of table names, return True, otherwise return False

        :param table_name: The name of the table you want to create
        :return: A list of all the tables in the database.
        """
        if table_name in self.get_tables_names():
            return True
        return False

    def relation_exist(self, rel_name):
        """
        It checks if the relation name is in the relations list.

        :param rel_name: The name of the relation
        :return: a boolean value.
        """
        if rel_name in self.relations:
            return True
        return False

    def is_sql_query(self, query: str):
        """
        If the query is a table view, it will return True, otherwise it will return False

        :param query: The query to be executed
        :type query: str
        :return: The function is_sql_query is returning a boolean value.
        """
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            if len(data) == 0:
                return False
            return True
        except:
            return False
