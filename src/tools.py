def clean_str(txt: str):
    while txt.startswith(" "):
        txt = txt[1:]
    while txt.endswith(" "):
        txt = txt[:-1]
    return txt


def clean_lst_str(lst: list):
    for i in range(len(lst)):
        lst[i] = clean_str(lst[i])
    return lst


def is_constant(arg):
    if arg.startswith("'") and arg.endswith("'"):
        return True
    return False


def error_rel_not_exist(rel: str, exp: str):
    return ["The relation '" + rel + "' in the (sub-)expression",
            "   " + exp,
            "does not exist"]


def error_column(relation, cols, col=None):
    error = ["Here is the list of column for the (sub-)expression:",
             "   " + relation + ":",
             "   " + str(cols)]
    if col is None:
        error.insert(0, "The first argument must be a column not a constant")

    elif type(col) == str:
        error.insert(0, "The column '" + col + "' is not present in the (sub-)expression")
    return error


def error_not_constant(relation, col: str):
    return ["'" + col + "' must be a constant not a column in the (sub-)expression:",
            "   " + relation]


def error_syntax(exp: str, elt: str):
    return ["Syntax error",
            "One of the " + elt + " is missing in the (sub-)expression",
            "   " + exp]


def error_operator(operator: str, exp: str, operators: list):
    return ["'" + operator + "' in the (sub-)expression:",
            "   " + exp,
            "is not an operator",
            "Here is the list of operators:",
            "   " + str(operators)]


