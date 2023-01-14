from tkinter import *
from tkinter.ttk import *

import connector

# global variables
lblInsertBox = []
entIns = []
sel = ""


# insert function for the insert popup
# gets all values from entIns array (entries in the popup window)
# creates an sql string with the current selected table and entries
# @TODO
# add functionality to show errors
def insert():
    strEntries = ""
    for ent in entIns:
        strEntries = strEntries + "\"" + ent.get() + "\", "

    strSql = "INSERT INTO " + sel + " VALUES(" + strEntries[:-2] + ");"
    cursor.execute(strSql)
    connection.commit()


# popup window for insertion
def open_popup():
    popup = Toplevel(root)
    popup.geometry("1200x300")
    popup.title("Insert new entry")

    # global selection variable that is selected with optSelector
    global sel
    sel = varSelector.get()

    # get column names from the selected table
    cursor.execute("show columns from " + sel)
    cols = cursor.fetchall()
    columns = []
    for col in cols:
        columns.append(col["Field"])

    # !Important reset the arrays that will be used in the next part
    global entIns, lblInsertBox
    lblInsertBox = []
    entIns = []

    # append to the label and entry arrays; newly created widgets and place them in a row with grid
    for i, col in enumerate(columns):
        lblInsertBox.append(Label(popup, text=col))
        lblInsertBox[i].grid(row=0, column=i, padx=10, pady=5)
        entIns.append(Entry(popup))
        entIns[i].grid(row=1, column=i, padx=10, pady=5)

    # insert button
    btnInsert = Button(popup, text="Insert", command=insert)
    btnInsert.grid(row=2, column=0, columnspan=4, padx=20, pady=20)

    # quit from popup button
    btnQuit = Button(popup, text="Quit", command=popup.destroy)
    btnQuit.grid(row=2, column=1, columnspan=4, padx=20, pady=20)


# execute custom queries in the database
def executeQuery():
    cursor.execute(query_entry.get())
    rows = cursor.fetchall()

    # clear the table
    for child in tree.get_children():
        tree.delete(child)

    # get table names from mysql
    keys = rows[0].keys()

    # create table tabs as many as you need
    # I had max 7 columns in my database
    # also clears the table from previous operations
    for i in range(8):
        tree.heading(str(i + 1), text="")

    # place column names in order
    for i, key in enumerate(keys):
        tree.heading(str(i + 1), text=str(key))

    # add the rows from the table
    for c, row in enumerate(rows):

        # accumulate all values in an array since pymysql returns query as dictionary
        values = []
        for col in row.values():
            values.append(col)

        tree.insert('', 'end', text=str(c + 1), values=values)

# show the selected table
# basically the same function as custom query but with varSelector for selecting a table
def selectTable():
    cursor.execute("SELECT * FROM " + varSelector.get())
    rows = cursor.fetchall()

    for child in tree.get_children():
        tree.delete(child)

    keys = rows[0].keys()

    for i in range(8):
        tree.heading(str(i + 1), text="")

    for i, key in enumerate(keys):
        tree.heading(str(i + 1), text=str(key))

    for c, row in enumerate(rows):
        values = []
        for col in row.values():
            values.append(col)

        tree.insert('', 'end', text=str(c + 1), values=values)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # initialize connection
    connection = connector.connect()
    cursor = connection.cursor()

    # main/root window
    root = Tk()
    root.title("MySQL Database Interface")
    root.geometry("1600x900")

    query_label = Label(root, text="Enter SQL Query:")
    query_label.grid(row=0, column=0, padx=30, pady=20)

    # for custom queries
    query_entry = Entry(root)
    query_entry.grid(row=0, column=1, padx=30, pady=20)

    # execute the query in query_entry
    execute_button = Button(root, text="Execute", command=executeQuery)
    execute_button.grid(row=1, column=0, padx=30, pady=20)

    lblSelector = Label(root, text="Select table to show/insert")
    lblSelector.grid(row=3, column=0, padx=30, pady=20)

    # sql query to get all tables in the database
    cursor.execute("SHOW TABLES")
    rows = cursor.fetchall()
    values = []
    for row in rows:
        for col in row.values():
            values.append(col)

    # variable for optSelector, you access values from this
    varSelector = StringVar(root)
    varSelector.set(values[0])

    # selector widget
    optSelector = OptionMenu(root, varSelector, *values)
    optSelector.grid(row=3, rowspan=1, column=1, padx=30, pady=20)

    # button to show selected table from optSelector
    btnSelectTable = Button(root, text="Show selected table", command=selectTable)
    btnSelectTable.grid(row=3, column=2, padx=30, pady=20)

    lblInsert = Label(root, text="Insert User")
    lblInsert.grid(row=4, column=0, columnspan=1, padx=30, pady=20)

    # button that opens insert popup
    btnInsPopup = Button(root, text="Insert New Entry", command=open_popup)
    btnInsPopup.grid(row=4, column=2, padx=30, pady=20)

    # table
    tree = Treeview(root, selectmode="browse")
    tree.grid(row=2, columnspan=3, padx=30, pady=20)

    # add placeholder columns to the table in main page
    tree["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8")
    tree["show"] = "headings"
    tree.column("1", width=80, anchor="c")
    tree.column("2", width=80, anchor="c")
    tree.column("3", width=80, anchor="c")
    tree.column("4", width=80, anchor="c")
    tree.column("5", width=80, anchor="c")
    tree.column("6", width=80, anchor="c")
    tree.column("7", width=80, anchor="c")
    tree.column("8", width=80, anchor="c")

    root.mainloop()
