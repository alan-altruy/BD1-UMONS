import os
from time import sleep


def first_menu(default: list):
    """
    It asks the user for the path of the database, and if the user
    doesn't enter anything, it uses the default database
    :return: The path of the database
    """
    clear()
    title("SPJRUD Translator")
    print("- Enter q for exit\n"
          "- For using default database, enter a name in this list: " + str(default)[1:-1] + "\n")
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


def menu_create_relation(already_exists: list):
    """
    It asks the user for a name and an expression, and returns them
    :return: The name and expression of the relation.
    """
    clear()
    title("Create SPJRUD relation")
    name = input("Name of the relation: ")
    wait()
    if name in already_exists:
        alert_box("An table/relation already has this name !")
        return menu_create_relation(already_exists)
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
    if len(tables) > 0 or len(tables) == 0:
        title("List of tables/relations")
        print_lst(tables)
        print_lst(relation)
        wait()
    else:
        alert_box("There is no table and relation !")


def print_list_relation(relations: dict):
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

    :param table_name: The name of the table to display
    :type table_name: str
    :param table: the table to display
    :type table: list
    """
    clear()
    display_size = os.get_terminal_size().columns
    title("Table " + table_name + ":")

    col_size = []
    to_verif_index = []
    tab_size = 0
    for i in range(len(table[0])):
        col_size.append(0)
        for j in range(len(table)):
            col_size[i] = max(len(str(table[j][i])), col_size[i])
        if (col_size[i] + 6) > (display_size/(len(table[0]))):
            to_verif_index.append(i)
        else:
            tab_size += col_size[i]
    display_size -= tab_size + 4 * len(col_size)
    nb = len(to_verif_index)
    for index in to_verif_index:
        col_size[index] = min(col_size[index], int(display_size/nb))
        tab_size += col_size[index]

    buffer = ""
    line = "╞"
    first_line = "╭"
    end_line = "╰"

    for i in range(len(table[0])):
        elt = table[0][i]
        if len(str(elt)) > col_size[i]:
            elt = elt[0:(col_size[i]-1)] + "…"
        buffer += ("│ {:^" + str(col_size[i]) + "} ").format(elt)
        line += ("═{:^" + str(col_size[i]) + "}═╪").format(col_size[i]*'═')
        first_line += ("─{:^" + str(col_size[i]) + "}─┬").format(col_size[i]*'─')
        end_line += ("─{:^" + str(col_size[i]) + "}─┴").format(col_size[i]*'─')
    buffer += "│"
    line = line[:-1] + "╡"
    first_line = first_line[:-1] + "╮"
    end_line = end_line[:-1] + "╯"

    print(first_line)
    print(buffer)
    print(line)
    buffer = ""

    table = table[1:]
    for i in range(len(table)):
        for j in range(len(table[i])):
            elt = str(table[i][j])
            if len(elt) > col_size[j]:
                elt = elt[:(col_size[j]-1)] + "…"
            buffer += ("│ {:" + str(col_size[j]) + "} ").format(str(elt))
        buffer += "│\n"
    if len(buffer) > 0:
        print(buffer[:-1])
    print(end_line)
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
    print(txt + "\n" + "‾" * len(txt))


def alert_box(txt):
    """
    It prints a box with a message in it

    :param txt: The text to be displayed in the alert box
    """
    if type(txt) == str:
        clear()
        print("╭" + "─" * (len(txt)) + "╮")
        print("│" + txt + "│")
        print("╰" + "─" * (len(txt)) + "╯")
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
