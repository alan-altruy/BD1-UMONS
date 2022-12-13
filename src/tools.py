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


def clean_cons(cons: str):
    return clean_str(cons[1:-1])


def is_constant(arg: str):
    if arg.startswith("'") and arg.endswith("'"):
        return True
    return False


def check_same_type(arg: str, type_col: str):
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
    error = ["The (sub-)expression",
             "   " + exp, "is invalid because " + args[0]]
    error.extend(args[1:])
    return error


def error_rel_not_exist(exp: str, rel: str, ):
    return _default_error(exp, ["the relation", "   " + rel, "does not exist"])


def error_column(exp: str, relation: str, col: str, cols: list):
    return _default_error(exp, ["the column", "   " + col, "is not present in the (sub-)expression:",
                                "   " + relation, "which contains the columns:", "   " + str(cols)])


def error_column_constant(exp: str, first_arg: str):
    return _default_error(exp, ["the first argument,", "   " + first_arg, "must be a column not a constant"])


def error_not_constant(exp: str, col: str):
    return _default_error(exp, ["the column", "   " + col, "must be a constant not a column"])


def error_syntax(exp: str, elt: str):
    return _default_error(exp, ["one of the ", "   " + elt, "is missing"])


def error_operator(exp: str, operator: str, operators: list):
    return _default_error(exp, ["the operator", "   " + operator, "is not an operator",
                                "Here is the list of operators:",
                                "   " + str(operators)])


def error_type_column(exp: str, col1: str, col2: str, schema: dict):
    return _default_error(exp, ["the type of column", "   " + col1 + ": " + schema[col1],
                                "is not the same as that of the column",
                                "   " + col2 + ": " + schema[col2]])


def error_arg_miss(exp: str):
    return _default_error(exp, ["at least one argument is missing", ])


def error_schema(exp: str, rel1: str, sch1: dict, rel2: str, sch2: dict):
    errors = ["the schema of", "   " + rel1, "which is"]
    for key in sch1.keys():
        errors.append("   - " + key + ": " + sch1[key])
    errors.extend(["is not the same as the one from", "   " + rel2, "which is"])
    for key in sch2.keys():
        errors.append("   - " + key + ": " + sch2[key])
    return _default_error(exp, errors)


def error_type(exp: str, arg: str, col: str, expected_type: str):
    return _default_error(exp, ["the type of", "   " + arg, "is not the one expected by the column",
                                "   " + col + ": " + expected_type])
