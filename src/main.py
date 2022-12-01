from spjrud import SJRUD
import os
from time import sleep


def show_table(s: SJRUD):
    os.system('clear')
    print("Show a table\n"
          "-----------------\n")
    table_name = input("Name of the table: ")
    s.show_table(s, table_name)

def execute(s: SJRUD):
    run = True
    while run:
        os.system('clear')
        print("SPJRUD Translator\n"
              "-----------------\n"
              "1. List of Table\n"
              "2. Show a table\n"
              "0. Back to Home\n")
        choice = input("Choice: ")
        if choice == '1':
            s.show_tables(s)
            input("\nPress any key to continue..")
        elif choice == '2':
            show_table(s)
        elif choice == '0':
            run = False


if __name__ == "__main__":
    run = True
    spjrud: SJRUD = SJRUD
    while run:
        os.system('clear')
        print("SPJRUD Translator\n"
              "-----------------\n"
              "- Enter q for exit\n"
              "- Do not enter anything to use the default database\n")
        db = input("Path of the database: ")
        if db == 'q':
            run = False
        elif db == '':
            spjrud.config(spjrud, "../resources/bd.db")
            execute(spjrud)
        else:
            try:
                open(db)
                spjrud.config(spjrud, db)
                execute(spjrud)
            except Exception as e:
                del e
                os.system('clear')
                print("! Path does not exist !")
                sleep(1)

