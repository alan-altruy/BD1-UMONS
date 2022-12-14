import os
from time import sleep


def first_menu():
    """
    It asks the user for the path of the database, and if the user
    doesn't enter anything, it uses the default database
    :return: The path of the database
    """
    clear()
    title("SPJRUD Translator")
    print("- Enter q for exit\n"
          "- Do not enter anything to use the default database\n")
    return input("Path of the database: ")


def main_menu():
    """
    It prints the main menu of the program
    :return: The user's choice.
    """
    clear()
    title("SPJRUD Translator")
    print("1. List of tables/relations\n"
          "2. Show a table/relation\n"
          "3. Create a SPJRUD relation\n"
          "4. List of SPJRUD relation\n"
          "5. Save a relation into the database\n"
          "0. Back to Home\n")
    return input("Choice: ")


def menu_show_table():
    """
    It clears the screen, prints a title, and asks the user for the name of the table they want to see
    :return: The name of the table.
    """
    clear()
    title("Show a table")
    return input("Name of the table: ")


def menu_create_expression():
    """
    It asks the user for a name and an expression, and returns them
    :return: The name and expression of the relation.
    """
    clear()
    title("Create SPJRUD expression")
    name = input("Name of the relation: ")
    expression = input("The expression: ")
    return name, expression


def menu_save_relation():
    """
    This function asks the user for the name of the relation to be saved
    :return: The name of the relation.
    """
    clear()
    title("Save a relation into the database")
    rel_name = input("Name of the relation: ")
    return rel_name


def print_list_table(tables: list, relation: list):
    """
    Prints a list of tables and relations

    :param tables: list of tables
    :type tables: list
    :param relation: list of tuples, each tuple is a row in the relation
    :type relation: list
    """
    clear()
    title("List of tables/relations")
    print_lst(tables)
    print_lst(relation)
    wait()


def print_list_expression(relations: dict):
    """
    It prints the list of relations

    :param relations: dict
    :type relations: dict
    """
    if len(relations.keys()) > 0:
        clear()
        title("List of relations")
        for key in relations.keys():
            print(" - " + key + " = " + relations[key][0] + ", sql = (" + relations[key][1] + ")")
        wait()
    else:
        alert_box("There are no saved relations !")


def print_table(table_name: str, table: list):
    """
    It prints a table

    :param table_name: The name of the table to be printed
    :type table_name: str
    :param table: the table to print
    :type table: list
    """
    clear()
    title("Table " + table_name + ":")
    buffer = ""
    line = "|" + (len(table[0]) * 23 - 1) * "-" + "|"
    print(line)
    for elt in table[0]:
        if len(str(elt)) > 18:
            elt = elt[0:18] + ".."
        buffer += "| {:^20} ".format(elt)
    print(buffer + "|")
    print(line)
    buffer = ""

    table = table[1:]
    for row in table:
        for elt in row:
            if len(str(elt)) > 18:
                elt = elt[0:18] + ".."
            buffer += "| {:^20} ".format(str(elt))
        buffer += "|\n"
    if len(buffer) > 0:
        print(buffer[:-1])
    print(line)
    wait()


def print_lst(lst: list):
    """
    `print_lst` takes a list of strings and prints each element of the list on a separate line

    :param lst: list
    :type lst: list
    """
    for elt in lst:
        print(" - " + elt)


def title(txt: str):
    """
    It prints a title

    :param txt: The title to be printed
    :type txt: str
    """
    print(txt + "\n" + "-" * len(txt) + "\n")


def alert_box(txt):
    """
    It prints a box with a message in it

    :param txt: The text to be displayed in the alert box
    """
    if type(txt) == str:
        clear()
        print("|" + "-" * (len(txt)) + "|")
        print("|" + txt + "|")
        print("|" + "-" * (len(txt)) + "|")
        sleep(1.5)
    elif len(txt) > 0:
        clear()
        title("Error")
        for error in txt:
            print(" " + error)
        wait()


def clear():
    """
    If the operating system is Windows, then the command to clear the screen is 'cls', otherwise it's 'clear'
    """
    txt = 'clear'
    if os.name == 'nt':
        txt = 'cls'
    os.system(txt)


def wait():
    """
    It waits for the user to press enter
    """
    input("\nPress enter to continue..")
