from spjrud import SPJRUD
import ui as basic_ui
import gui


def show_table(db: SPJRUD):
    """
    It shows a table or a relation

    :param db: SPJRUD main object
    :type db: SPJRUD
    """
    table_name = ui.menu_show_table()
    if db.table_exist(table_name):
        ui.print_table(table_name, db.get_table(table_name))
    elif db.relation_exist(table_name):
        ui.print_table(table_name, db.get_relation(table_name))
    else:
        ui.alert_box("The table/relation does not exist !")


def create_spjrud_expression(db: SPJRUD):
    """
    It creates a new expression in the database

    :param db: SPJRUD main object
    :type db: SPJRUD
    """
    already_exists = db.get_tables_names()
    already_exists.extend(db.get_relations_names())

    (name, expression) = ui.menu_create_relation(already_exists)
    ui.alert_box(db.create_expression(name, expression))


def save_relation_into_db(db: SPJRUD):
    """
    > This function saves a relation into the database

    :param db: SPJRUD main object
    :type db: SPJRUD
    """
    rel_name = ui.menu_save_relation()
    ui.alert_box(db.save_relation_into_db(rel_name))


def launch_main_menu(db: SPJRUD):
    """
    It's a loop that asks the user for a command, and then executes that command

    :param db: SPJRUD main object
    :type db: SPJRUD
    """
    is_running = True
    while is_running:
        choice = ui.main_menu()
        if choice == '1':
            ui.print_list_table(db.get_tables_names(), db.get_relations_names())
        elif choice == '2':
            show_table(db)
        elif choice == '3':
            create_spjrud_expression(db)
        elif choice == '4':
            ui.print_list_relation(db.get_relations())
        elif choice == '5':
            save_relation_into_db(db)
        elif choice == '0':
            is_running = False
        elif choice == 'q':
            return False
        elif db.is_sql_query(choice):
            ui.print_table("[Your query]", db.get_table_from_query(choice))
    return True


global ui

if __name__ == "__main__":
    run = True
    selected_ui = input("Select the UI (1. Console, 2. GUI): ")
    files_names = ["default", "cinema", "dallas-police"]
    spjrud: SPJRUD = SPJRUD()
    if selected_ui == "2":
        gui.GUI(spjrud, files_names)
        run = False
    else:
        ui = basic_ui
    while run:
        file_name = ui.first_menu(files_names)
        if file_name == 'q':
            run = False
        elif file_name in files_names:
            spjrud.config(str(__file__)[:-11] + "resources/" + file_name + ".db")
            run = launch_main_menu(spjrud)
        else:
            try:
                open(file_name)
                spjrud.config(file_name)
                launch_main_menu(spjrud)
            except:
                ui.alert_box("! Path or file does not exist !")
