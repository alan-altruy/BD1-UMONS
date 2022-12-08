import os
from time import sleep


def first_menu():
    clear()
    title("SPJRUD Translator")
    print("- Enter q for exit\n"
          "- Do not enter anything to use the default database\n")
    return input("Path of the database: ")


def main_menu():
    clear()
    title("SPJRUD Translator")
    print("1. List of Tables/Relations\n"
          "2. Show a table/relation\n"
          "3. Create a SPJRUD expression\n"
          "4. List of SPJRUD expression\n"
          "5. Execute a SPJRUD expression\n"
          "0. Back to Home\n")
    return input("Choice: ")


def menu_show_table():
    clear()
    title("Show a table")
    return input("Name of the table: ")


def menu_create_expression():
    clear()
    title("Create SPJRUD expression")
    name = input("Name of the relation: ")
    expression = input("The expression: ")
    return name, expression


def print_list_table(tables: list):
    clear()
    title("List of tables")
    print_lst(tables)
    # TODO list of relations
    wait()


def print_list_expression(expressions: dict):
    if len(expressions.keys()) > 0:
        clear()
        title("List of expressions")
        for key in expressions.keys():
            print(" - " + key + " = " + expressions[key])
        wait()
    else:
        alert_box("There are no saved expressions !")


def print_table(table_name: str, table: list):
    clear()
    title("Table " + table_name + ":")
    buffer = ""
    print("|" + (len(table[0]) * 23 - 1) * "-" + "|")
    for elt in table[0]:
        if len(str(elt)) > 18:
            elt = elt[0:18] + ".."
        buffer += "| {:^20} ".format(elt)
    print(buffer + "|")
    print("|" + (len(table[0]) * 23 - 1) * "-" + "|")
    buffer = ""

    table = table[1:]
    for line in table:
        for elt in line:
            if len(str(elt)) > 18:
                elt = elt[0:18] + ".."
            buffer += "| {:^20} ".format(str(elt))
        buffer += "|\n"
    print(buffer[:-1])
    print("|" + (len(table[0]) * 23 - 1) * "-" + "|")

    wait()


def print_lst(lst: list):
    for elt in lst:
        print(" - " + elt)


def title(txt: str):
    print(txt + "\n" + "-" * len(txt) + "\n")


def alert_box(txt: str):
    clear()
    print("|" + "-" * (len(txt)) + "|")
    print("|" + txt + "|")
    print("|" + "-" * (len(txt)) + "|")
    sleep(1.5)


def clear():
    os.system("clear")


def wait():
    input("\nPress any key to continue..")
