def clean_str(txt: str):
    """
    It removes all leading and trailing spaces from a string

    :param txt: The text to be cleaned
    :type txt: str
    :return: the cleaned string.
    """
    while txt.startswith(" "):
        txt = txt[1:]
    while txt.endswith(" "):
        txt = txt[:-1]
    return txt


def clean_lst_str(lst: list):
    """
    It takes a list of strings and cleans each string in the list

    :param lst: list
    :type lst: list
    :return: A list of strings
    """
    for i in range(len(lst)):
        lst[i] = clean_str(lst[i])
    return lst


def clean_cons(cons: str):
    """
    It takes a string of the form 'constant' and returns a string of the form: constant

    :param cons: the constant string
    :type cons: str
    :return: The constant cleaned
    """
    return clean_str(cons[1:-1])


def is_constant(arg: str):
    """
    `is_constant` returns `True` if the argument is a constant, and `False` otherwise

    :param arg: The argument to be checked
    :type arg: str
    :return: The function is_constant is returning a boolean value.
    """
    if arg.startswith("'") and arg.endswith("'"):
        return True
    return False


def check_same_type(arg: str, type_col: str):
    """
    If the argument is a number, check if the column type is an integer, if not, check if the argument is a float,
    if not, check if the column type is text

    :param arg: the argument to be checked
    :type arg: str
    :param type_col: the type of the column
    :type type_col: str
    :return: a boolean value.
    """
    if arg.isnumeric():
        return 'integer' == type_col
    else:
        try:
            float(arg)
            return 'real' == type_col
        except Exception:
            pass
    return type_col == 'text'


def _default_error(exp: str, args: list):
    """
    It takes a string and a list of strings, and returns a list of strings

    :param exp: the expression being evaluated
    :type exp: str
    :param args: a list of strings, each of which is an argument to the error message
    :type args: list
    :return: A string that contains the error message.
    """
    error = ["The (sub-)expression",
             "   " + exp, "is invalid because " + args[0]]
    error.extend(args[1:])
    return error


def error_rel_not_exist(exp: str, rel: str, ):
    """
    It returns an error message for when a relation does not exist

    :param exp: the expression that was being evaluated
    :type exp: str
    :param rel: the name of the relation
    :type rel: str
    :return: A string that is the error message.
    """
    return _default_error(exp, ["the relation", "   " + rel, "does not exist"])


def error_column(exp: str, relation: str, col: str, cols: list):
    """
    It returns an error message for the case where a column is not present in a relation

    :param exp: the expression that is being checked
    :type exp: str
    :param relation: the name of the relation
    :type relation: str
    :param col: the column that is not present in the relation
    :type col: str
    :param cols: the list of columns in the relation
    :type cols: list
    :return: The error message.
    """
    return _default_error(exp, ["the column", "   " + col, "is not present in the (sub-)expression:",
                                "   " + relation, "which contains the columns:", "   " + str(cols)])


def error_column_constant(exp: str, first_arg: str):
    """
    It takes an expression and an argument and returns an error

    :param exp: the expression that is being evaluated
    :type exp: str
    :param first_arg: the first argument to the function
    :type first_arg: str
    :return: A string that is the error message.
    """
    return _default_error(exp, ["the first argument,", "   " + first_arg, "must be a column not a constant"])


def error_not_constant(exp: str, col: str):
    """
    It takes a string and a column name and returns an error message

    :param exp: the expression that was being evaluated
    :type exp: str
    :param col: the column name
    :type col: str
    :return: A string that contains the error message.
    """
    return _default_error(exp, ["the column", "   " + col, "must be a constant not a column"])


def error_syntax(exp: str, elt: str):
    """
    Return an error for missing element in the expression

    :param exp: the expression that is being parsed
    :type exp: str
    :param elt: the element that is missing
    :type elt: str
    :return: A string that is a formatted error message.
    """
    return _default_error(exp, ["one of the ", "   " + elt, "is missing"])


def error_operator(exp: str, operator: str, operators: list):
    """
    It returns an error message for when an operator is not an operator

    :param exp: the expression that was being parsed
    :type exp: str
    :param operator: the operator that is not an operator
    :type operator: str
    :param operators: a list of operators
    :type operators: list
    :return: The error message for when an operator is not an operator.
    """
    return _default_error(exp, ["the operator", "   " + operator, "is not an operator",
                                "Here is the list of operators:",
                                "   " + str(operators)])


def error_type_column(exp: str, col1: str, col2: str, schema: dict):
    """
    It returns an error message that says the type of column `col1` is not the same as that of column `col2`

    :param exp: the expression that is being checked
    :type exp: str
    :param col1: the name of the first column
    :type col1: str
    :param col2: the column that is being compared to col1
    :type col2: str
    :param schema: a dictionary of column names to types
    :type schema: dict
    :return: A string that contains the error message.
    """
    return _default_error(exp, ["the type of column", "   " + col1 + ": " + schema[col1],
                                "is not the same as that of the column",
                                "   " + col2 + ": " + schema[col2]])


def error_arg_miss(exp: str):
    """
    It returns a default error message for the case where at least one argument is missing

    :param exp: the expression that was passed to the function
    :type exp: str
    :return: A string that contains the error message.
    """
    return _default_error(exp, ["at least one argument is missing", ])


def error_schema(exp: str, rel1: str, sch1: dict, rel2: str, sch2: dict):
    """
    It takes in two schemas and two relation names, and returns a string that describes the error

    :param exp: the expression that was being evaluated
    :type exp: str
    :param rel1: the name of the first relation
    :type rel1: str
    :param sch1: the schema of the first relation
    :type sch1: dict
    :param rel2: the name of the relation that is being compared to
    :type rel2: str
    :param sch2: the schema of the relation that is being joined with
    :type sch2: dict
    :return: A string that contains the error message.
    """
    errors = ["the schema of", "   " + rel1, "which is"]
    for key in sch1.keys():
        errors.append("   - " + key + ": " + sch1[key])
    errors.extend(["is not the same as the one from", "   " + rel2, "which is"])
    for key in sch2.keys():
        errors.append("   - " + key + ": " + sch2[key])
    return _default_error(exp, errors)


def error_type(exp: str, arg: str, col: str, expected_type: str):
    """
    It returns an error message for the case where the type of the argument is not the one expected by the column

    :param exp: the expression that is being evaluated
    :type exp: str
    :param arg: the name of the argument
    :type arg: str
    :param col: the name of the column
    :type col: str
    :param expected_type: the type of the column
    :type expected_type: str
    :return: A string.
    """
    return _default_error(exp, ["the type of", "   " + arg, "is not the one expected by the column",
                                "   " + col + ": " + expected_type])
