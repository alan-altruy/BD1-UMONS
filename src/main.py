from spjrud import SPJRUD
import ui


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
    (name, expression) = ui.menu_create_expression()
    ui.alert_box(db.create_expression(name, expression))


def save_relation_into_db(db: SPJRUD):
    """
    > This function saves a relation into the database

    :param db: SPJRUD main object
    :type db: SPJRUD
    """
    rel_name = ui.menu_save_relation()
    ui.alert_box(db.save_relation_into_db(rel_name))


def execute(db: SPJRUD):
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
            ui.print_list_expression(db.get_relations())
        elif choice == '5':
            save_relation_into_db(db)
        elif choice == '0':
            is_running = False
        elif db.is_sql_query(choice):
            ui.print_table("[Your query]", db.get_table_from_query(choice))


if __name__ == "__main__":
    run = True
    spjrud: SPJRUD = SPJRUD()
    while run:
        file_name = ui.first_menu()
        if file_name == 'q':
            run = False
        elif file_name == '':
            spjrud.config(str(__file__)[:-11]+"resources/bd.db")
            execute(spjrud)
        else:
            try:
                open(file_name)
                spjrud.config(file_name)
                execute(spjrud)
            except:
                ui.alert_box("! Path or file does not exist !")
