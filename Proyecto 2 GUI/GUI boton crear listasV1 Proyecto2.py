import tkinter as tk

PeopleList = []
Lists = []

# Funciones para el menu de crear nombre de la lista #

# Funciones para los botones de la ventana de Crear listas menu #

def add_person():
    global TextBox_WritePeopleName, listbox_ListofPeople
    name = TextBox_WritePeopleName.get()
    if name != "":
        listbox_ListofPeople.insert(tk.END, name)
        TextBox_WritePeopleName.delete(0, tk.END)

def delete_person():
    global listbox_ListofPeople
    selection = listbox_ListofPeople.curselection()
    if len(selection) != 0:
        index = selection[0]
        listbox_ListofPeople.delete(index)

def clear_list():
    global listbox_ListofPeople
    listbox_ListofPeople.delete(0, tk.END)

# Funciones de los botones en la ventana principal #

def DEFCreateList_MainPopup():
    global TextBox_WritePeopleName, listbox_ListofPeople
    MainpopupCreatelist = tk.Toplevel()
    MainpopupCreatelist.geometry("400x300")
    MainpopupCreatelist.title("Crear listas menu") 

    # Etiqueta para agregar personas
    label_EnterPeopleName = tk.Label(MainpopupCreatelist, text="Introduzca el nombre de las personas:")
    label_EnterPeopleName.pack(pady=10)
    label_EnterPeopleName.place(x=25, y=25)
    
    # Caja de texto para agregar personas
    TextBox_WritePeopleName = tk.Entry(MainpopupCreatelist)
    TextBox_WritePeopleName.pack(pady=5)
    TextBox_WritePeopleName.place(x=60, y=50)

    # Etiqueta para la lista de personas
    label_ListOfPeople = tk.Label(MainpopupCreatelist, text="Lista de Personas:")
    label_ListOfPeople.pack(pady=10)
    label_ListOfPeople.place(x=70, y=75)

    # Lista de personas
    listbox_ListofPeople = tk.Listbox(MainpopupCreatelist)
    listbox_ListofPeople.pack(pady=5)
    listbox_ListofPeople.place(x=60, y=100)

    # Botones de la ventana Crear lista
    # Botón para agregar personas
    button_add = tk.Button(MainpopupCreatelist, text="Agregar", command=add_person)
    button_add.pack(pady=5)
    button_add.place(x=250, y=60)

    # Boton para eliminar cada personas seleccionada por el mouse
    button_deletePerson = tk.Button(MainpopupCreatelist, text="Eliminar persona", command=delete_person)
    button_deletePerson.pack(pady=7)
    button_deletePerson.place(x=250, y=100)

    # boton para limpiar toda la lista
    button_CleanList = tk.Button(MainpopupCreatelist, text="Limpiar lista", command=clear_list)
    button_CleanList.pack(pady=8)
    button_CleanList.place(x=250, y=140)

    # Botón para cerrar la ventana emergente o volver atras(no se guarda)
    button_CloseWindow = tk.Button(MainpopupCreatelist, text="Volver atrás", command=MainpopupCreatelist.destroy)
    button_CloseWindow.pack(pady=9)
    button_CloseWindow.place(x=250, y=180)



def DEFCheckLists_MainPopup():
    popup = tk.Toplevel()
    popup.geometry("400x300")
    popup.title("Listas Creadas") 


Main_window = tk.Tk()

# Ventana principal #
Main_window.title("Main menu")
Main_window.geometry("500x500")

# Botones de ventana principal #
MainButton_CreateList = tk.Button(Main_window, text="Crear listas", command=DEFCreateList_MainPopup)
MainButton_CreateList.place(x=60, y=50)

MainButton_CheckLists = tk.Button(Main_window, text="Ver listas Creadas", command=DEFCheckLists_MainPopup)
MainButton_CheckLists.place(x=60, y=90)

Main_window.mainloop()

