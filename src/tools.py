def clean_str(txt: str):
    while txt.startswith(" "):
        txt = txt[1:]
    while txt.endswith(" "):
        txt = txt[:-1]
    return txt


def clean_lst_str(lst: list):
    for i in range (len(lst)):
        lst[i] = clean_str(lst[i])
    return lst


def is_constant(arg):
    if arg.startswith("'") and arg.endswith("'"):
        return True
    return False
