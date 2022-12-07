from spjrud import SJRUD
import os
import gui


def show_table(db: SJRUD):
    table_name = gui.menu_show_table()
    if db.table_exist(table_name):
        gui.print_table(table_name, db.get_table(table_name))
    else:
        gui.alert_box("The table does not exist !")


def create_spjrud_expression(db):
    (name, expression) = gui.menu_create_expression()
    gui.alert_box(db.create_expression(name, expression))


def execute(db: SJRUD):
    run = True
    while run:
        choice = gui.main_menu()
        if choice == '1':
            gui.print_list_table(db.get_tables())
        elif choice == '2':
            show_table(db)
        elif choice == '3':
            create_spjrud_expression(db)
        elif choice == '4':
            gui.print_list_expression(db.get_expressions())
        elif choice == '5':
            pass #TODO
        elif choice == '0':
            run = False


if __name__ == "__main__":
    run = True
    spjrud: SJRUD = SJRUD()
    while run:
        os.system('clear')
        db = gui.first_menu()
        if db == 'q':
            run = False
        elif db == '':
            spjrud.config("../resources/bd.db")
            execute(spjrud)
        else:
            try:
                open(db)
                spjrud.config(db)
                execute(spjrud)
            except Exception as e:
                del e
                gui.alert_box("! Path or file does not exist !")
