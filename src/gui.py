import os.path
import tktable
import tkinter as tk
from tkinter.filedialog import askopenfilename
from spjrud import SPJRUD


class GUI(tk.Tk):
    spjrud: SPJRUD
    default: list

    def __init__(self, spjrud: SPJRUD, default: list):
        super().__init__()
        self.title("SPJRUD Translator")
        self.geometry("800x600")
        self.frame = tk.Frame(self)
        self.db_path = tk.StringVar()
        self.spjrud = spjrud
        self.default = default
        self.first_menu()

    def clear(self):
        """
        It clears the screen
        """
        self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.pack()

    def first_menu(self):
        """
        It asks the user for the path of the database, and if the user
        doesn't enter anything, it uses the default database (gui version)
        :return: The path of the database
        """
        self.clear()
        for database in self.default:
            tk.Button(self.frame, text=database, command=lambda database=database: self.selected_file(name=database)).pack()
        tk.Button(self.frame, text="Open File", command=lambda: self.selected_file(name=None)).pack()
        self.mainloop()

    def selected_file(self, name=None):
        if name is None:
            path = askopenfilename(defaultextension="db", filetypes=[("Database files", "*.db")])
        else:
            path = os.path.abspath("../resources/" + name + ".db")
        try:
            open(path)
            self.spjrud.config(path)
            self.main_menu()
        except:
            self.alert_box("! Path or file does not exist !")
            self.first_menu()

    def main_menu(self):
        """
        It prints the main menu of the program
        :return: The user's choice.
        """
        self.clear()
        tk.Button(self.frame, text="Tables/relations", command=lambda: self.print_list_table()).pack()
        tk.Button(self.frame, text="Create a SPJRUD relation", command=lambda: self.create_spjrud_expression()).pack()
        tk.Button(self.frame, text="List of SPJRUD relation", command=lambda: self.print_list_relation()).pack()
        tk.Button(self.frame, text="Back to Home", command=lambda: self.first_menu()).pack()
        self.mainloop()

    def print_list_table(self):
        """
        It prints the list of tables and relations
        """
        self.clear()
        list_tables = self.spjrud.get_tables_names()
        list_relations = self.spjrud.get_relations_names()
        tk.Label(self.frame, text="Tables: ").pack()
        for table in list_tables:
            tk.Button(self.frame, text=table, command=lambda table=table: self.show_table(table)).pack()
        tk.Label(self.frame, text="Relations: ").pack()
        for relation in list_relations:
            tk.Button(self.frame, text=relation, command=lambda relation=relation: self.show_table(relation)).pack()
        self.mainloop()

    def create_spjrud_expression(self):
        """
        It asks the user for a name and an expression, and returns them
        :return: The name and expression of the relation.
        """
        self.clear()
        tk.Label(self.frame, text="Create SPJRUD relation").grid(row=0, column=0, columnspan=2)
        name = tk.Entry(self.frame)
        tk.Label(self.frame, text="Name of the relation: ").grid(row=0, column=0)
        name.grid(row=0, column=1)
        tk.Label(self.frame, text="The expression: ").grid(row=1, column=0)
        expression = tk.Entry(self.frame)
        expression.grid(row=1, column=1)
        (tk.Button(self.frame, text="Create", command=lambda: self.save_relation(name.get(), expression.get()))
         .grid(row=2, column=0, sticky=tk.E))
        tk.Button(self.frame, text="Back", command=lambda: self.main_menu()).grid(row=2, column=1, sticky=tk.W)

        self.mainloop()

    def save_relation(self, name, expression):
        """
        It saves a relation into the database
        :param name: The name of the relation
        :param expression: The expression of the relation
        """
        self.alert_box(self.spjrud.create_expression(name, expression))

    def save_relation_into_db(self, name):
        """
        It saves a relation into the database
        :param name: The name of the relation
        """
        self.alert_box(self.spjrud.save_relation_into_db(name))

    def print_list_relation(self):
        """
        It prints the list of relations
        """
        self.clear()
        dic_relations = self.spjrud.get_relations()
        list_relations = self.spjrud.get_relations_names()
        list_tables = self.spjrud.get_tables_names()
        for relation in list_relations:
            tk.Label(self.frame, text=(relation, ":", "\n".join(dic_relations[relation]))).grid(row=0, column=0)
            tk.Button(self.frame, text="Show", command=lambda relation=relation: self.show_table(
                relation)).grid(row=0, column=1)
            if relation not in list_tables:
                tk.Button(self.frame, text="Save", command=lambda relation=relation: self.
                          save_relation_into_db(relation)).grid(row=0, column=2)
        tk.Button(self.frame, text="Back", command=lambda: self.main_menu()).pack()
        self.mainloop()

    def show_table(self, table_name):
        """
        It shows a table or a relation
        :param table_name: The name of the table
        """
        if self.spjrud.table_exist(table_name):
            self.print_table(table_name, self.spjrud.get_table(table_name))
        elif self.spjrud.relation_exist(table_name):
            self.print_table(table_name, self.spjrud.get_relation(table_name))
        else:
            self.alert_box("The table/relation does not exist !")

    def print_table(self, table_name, table):
        """
        It prints a table
        :param table_name: The name of the table
        :param table: The table to be printed
        """
        self.clear()
        tk.Label(self.frame, text=table_name, font=("Arial", 20, "bold")).pack()
        header = table[0]
        rows = table[1:]

        display_size = self.winfo_width() - 50
        col_size = display_size / len(header)

        table = tktable.Table(self.frame, columns=header, headings_bold=True, col_width=int(col_size))

        for row in rows:
            table.insert_row(row)
        table.pack()

        tk.Button(self.frame, text="Back", command=lambda: self.main_menu()).pack()
        tk.Button(self.frame, text="Refresh", command=lambda: self.show_table(table_name)).pack()
        self.mainloop()

    @staticmethod
    def alert_box(msg):
        """
        It shows a message to the user
        :param msg: The message to be shown
        """
        if type(msg) is str:
            tk.messagebox.showinfo("Alert", msg)
        elif len(msg) > 0:
            tk.messagebox.showinfo("Alert", "\n".join(msg))
