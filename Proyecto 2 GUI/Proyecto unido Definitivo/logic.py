from tkinter import Button, Entry, END, ttk, messagebox, simpledialog, Toplevel,Label
from tkinter.filedialog import askopenfilename

# Listas globales
lista_participantes = set()
Agend = []

def open_data(btn1:Button, btn2:Button):
    """
    Abre un archivo de texto seleccionado por el usuario y lee los datos.

    Agrs:
    - btn1: Objeto Button que representa el boton participantes.
    - btn2: Objeto Button que representa el boton reconocimiento.

    Funcionalidad:
    1. Muestra un diálogo para que el usuario seleccione un archivo de texto.
    2. Si el usuario no selecciona ningún archivo, la función retorna.
    3. Abre el archivo seleccionado en modo lectura.
    4. Lee los datos del archivo y los almacena en la variable 'data'.
    5. Evalúa los datos almacenados en 'data[0]' y los asigna a la variable global 'Agend'.
    6. Evalúa los datos almacenados en 'data[1]' y los asigna a la variable global 'lista_participantes'.
    7. Configura el estado de 'btn1' y 'btn2' como 'normal'.
    8. Cierra el archivo.

    """
    global Agend, lista_participantes
    file = askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if not file:
        return
    with open(file, 'r') as f:
        data = f.read().splitlines()
        Agend = eval(data[0])
        lista_participantes = eval(data[1])
    btn1.config(state="normal")
    btn2.config(state="normal")
    f.close()


def section_creation(sec: str, btn1: Button, btn2: Button, box: Entry):
    """
    Crea un nuevo apartado en la agenda.

    Args:
        sec (str): Nombre del apartado.
        btn1 (Button): Botón Apartado.
        btn2 (Button): Botón Punto.
        box (Entry): Cuadro de entrada Apartado.

    Returns:
        list: La lista Agend actualizada.
    """
    global Agend

    if sec == "":
        clean(box)
        messagebox.showinfo("Ningún valor", "No ingresó ningún valor")
        return

    if Agend != []:
        for x in Agend:
            if x["Section"] == sec:
                clean(box)
                messagebox.showinfo("Apartado repetido", "Ya existe un apartado con el mismo nombre")
                print(Agend)
                return

    Agend.append({"Section": sec, "Points": []})
    btn1.config(state="disabled")
    btn2.config(state="normal")
    clean(box)
    print(Agend)
    return Agend

def show_agend(table):
    """
    Muestra los apartados de la agenda en una tabla.

    Parámetros:
    - table: Objeto ttk.Treeview que representa la tabla donde se mostrarán los apartados.

    Funcionalidad:
    1. Si la lista 'Agend' está vacía, la función retorna.
    2. Por cada elemento 'x' en 'Agend', inserta en la tabla una nueva fila con el valor de 'x["Section"]'.
    """

    if Agend == []:
        return
    for x in Agend:
        table.insert("", END, values=(x["Section"]))


def show_parts(table):
    """
    Muestra los participantes en una tabla.

    Agrs:
    - table: Objeto ttk.Treeview que representa la tabla donde se mostrarán los participantes.

    Funcionalidad:
    1. Si el conjunto 'lista_participantes' está vacío, la función retorna.
    2. Por cada elemento 'x' en 'lista_participantes', inserta en la tabla una nueva fila con el valor de 'x'.
    """

    if lista_participantes == set():
        return
    for x in lista_participantes:
        table.insert(END, x)

        


def point_creation(poi: str, message, btn1: Button, btn2: Button, box: Entry, table: ttk):
    """
    Crea un nuevo punto en el apartado actual de la agenda.

    Args:
        poi (str): Nombre del punto.
        message: Mensaje de confirmación.
        btn1 (Button): Botón Apartado.
        btn2 (Button): Botón Punto.
        box (Entry): Cuadro de entrada punto.
        table (ttk): Tabla de puntos.

    Returns:
        None
    """
    global Agend, cont

    if poi == "":
        clean(box)
        messagebox.showinfo("Ningún valor", "No ingresó ningún valor")
        return

    if Agend[0]["Points"] != []:
        for e in Agend:
            for x in e["Points"]:
                if x["Name"] == poi:
                    clean(box)
                    messagebox.showinfo("Punto repetido", "Ya existe un punto con el mismo nombre")
                    print(Agend)
                    return

    if message:
        point = {"Name": poi, "Participations": []}
        Agend[-1]["Points"].append(point)
        print(Agend)
    else:
        point = {"Name": poi, "Participations": []}
        Agend[-1]["Points"].append(point)
        btn1.config(state="normal")
        btn2.config(state="disabled")
        generate_table(table)
        print(Agend)

    clean(box)


def generate_table(table: ttk):
    """
    Genera la tabla de apartados en la interfaz.

    Args:
        table (ttk): Tabla de apartados.

    Returns:
        None
    """
    table.delete(*table.get_children())
    for x in Agend:
        table.insert("", END, values=(x["Section"]))

def generate_table_points(tablep: ttk, section):
    """
    Genera la tabla de puntos en la interfaz.

    Args:
        tablep (ttk): Tabla de puntos.
        section: Apartado seleccionado.

    Returns:
        None
    """
    tablep.delete(*tablep.get_children())
    for x in Agend:
        if x["Section"] == section:
            for e in x["Points"]:
                tablep.insert("", END, values=(e["Name"]))


def show_point(table: ttk):
    """
    Muestra la tabla de puntos en la interfaz.

    Args:
        table (ttk): Tabla de puntos.

    Returns:
        None
    """
    table.delete(*table.get_children())
    for x in Agend:
        for e in x["Points"]:
            table.insert("", END, values=(e["Name"]))


def edit_section(table, item_id):
    """
    Edita un apartado de la agenda.

    Args:
        table: Tabla de apartados.
        item_id: ID del elemento a editar.

    Returns:
        None
    """
    global Agend
    section = table.item(item_id)["values"][0]
    new_section = simpledialog.askstring("Editar apartado", "Ingrese el nuevo valor:", initialvalue=section)
    if new_section:
        table.set(item_id, column="Apartado", value=new_section)
        for x in Agend:
            if x["Section"] == section:
                x["Section"] = new_section
                break


def delete_section(table, item_id):
    """
    Elimina un apartado de la agenda.

    Args:
        table: Tabla de apartados.
        item_id: ID del elemento a eliminar.

    Returns:
        None
    """
    section = table.item(item_id)["values"][0]
    confirmed = messagebox.askyesno("Eliminar apartado", "¿Está seguro que desea eliminar el apartado seleccionado?\n ¡También se eliminarán los puntos enlazados!")
    if confirmed:
        table.delete(item_id)
        for x in Agend:
            if x["Section"] == section:
                Agend.remove(x)
                break


def edit_point(table, item_id):
    """
    Edita un punto de la agenda.

    Args:
        table: Tabla de puntos.
        item_id: ID del elemento a editar.

    Returns:
        None
    """
    global Agend
    point = table.item(item_id)["values"][0]
    new_point = simpledialog.askstring("Editar punto", "Ingrese el nuevo valor:", initialvalue=point)
    if new_point:
        table.set(item_id, column="Puntos", value=new_point)
        for x in Agend:
            for e in x["Points"]:
                if e["Name"] == point:
                    e["Name"] = new_point
                    break


def delete_point(table, item_id):
    """
    Elimina un punto de la agenda.

    Args:
        table: Tabla de puntos.
        item_id: ID del elemento a eliminar.

    Returns:
        None
    """
    point = table.item(item_id)["values"][0]
    confirmed = messagebox.askyesno("Eliminar punto", "¿Está seguro que desea eliminar el punto seleccionado?")
    if confirmed:
        table.delete(item_id)
        for x in Agend:
            for e in x["Points"]:
                if e["Name"] == point:
                    x["Points"].remove(e)
                    break

def agregar_participacion(point, text, part):
    """
    Agrega una participación a un punto de la agenda.

    Args:
        point: Nombre del punto.
        text: Texto de la participación.
        part: Participante.

    Returns:
        None
    """
    global Agend

    for x in Agend:
        for e in x["Points"]:
            if e["Name"] == point:
                e["Participations"].append({"Participante": part, "text": text})
                printa()
                break


def tablepart(table: ttk):
    """
    Genera la tabla de participantes en la interfaz.

    Args:
        table (ttk): Tabla de participantes.

    Returns:
        None
    """
    global lista_participantes
    for x in lista_participantes:
        table.insert("", END, values=x)


def clean(box: Entry):
    """
    Limpia el contenido del cuadro de entrada.

    Args:
        box (Entry): Cuadro de entrada.

    Returns:
        None
    """
    box.delete(0, END)


def printa():
    """
    Imprime el contenido de la agenda.

    Returns:
        None
    """
    global Agend
    print(Agend)


def add_person(TextBox_WritePeopleName, listbox_ListofPeople):
    """
    Agrega una persona a la lista de participantes.

    Args:
        TextBox_WritePeopleName (Entry): Cuadro de entrada con el nombre de la persona.
        listbox_ListofPeople: Lista donde se mostrarán los participantes.

    Returns:
        None
    """
    name = TextBox_WritePeopleName.get()
    if name != "":
        listbox_ListofPeople.insert(END, name)
        TextBox_WritePeopleName.delete(0, END)


def delete_person(listbox_ListofPeople):
    """
    Elimina una persona de la lista de participantes.

    Args:
        listbox_ListofPeople: Lista de participantes.

    Returns:
        None
    """
    global lista_participantes
    selection = listbox_ListofPeople.curselection()
    selec = listbox_ListofPeople.get(selection)
    if lista_participantes != set():
        lista_participantes.remove(selec)
    if len(selection) != 0:
        index = selection[0]
        listbox_ListofPeople.delete(index)


def clear_list(listbox_ListofPeople):
    """
    Limpia la lista de participantes.

    Args:
        listbox_ListofPeople: Lista de participantes.

    Returns:
        None
    """
    listbox_ListofPeople.delete(0, END)


def save_list(listbox_ListofPeople):
    """
    Guarda los participantes de la lista.

    Args:
        listbox_ListofPeople: Lista de participantes.

    Returns:
        None
    """
    global lista_participantes
    lista = list(listbox_ListofPeople.get(0, END))
    if lista:
        for x in lista:
            lista_participantes.add(x)
    print(lista_participantes)


def mostrar_documento_tkinter():
    """
    Abre el archivo 'archivo.txt', lee su contenido y muestra el contenido en una ventana de tkinter.

    Returns:
        None
    """
    ventana = Toplevel()
    label = Label(ventana, wraplength=400)
    label.pack(padx=20, pady=20)

    ventana.iconbitmap("Imagenes/correcto.ico")

    with open('archivo.txt', 'r') as f:
        contenido = f.read()
        label.config(text=contenido)


def generar_archivo_texto():
    """
    Genera un archivo de texto llamado 'archivo.txt' a partir de los datos en la variable global Agend.

    Returns:
        None
    """
    global Agend
    with open("archivo.txt", 'w') as f:
        for item in Agend:
            section = item.get('Section', '')
            f.write(f"=== {section} ===\n")
            points = item.get('Points', [])
            if not points:
                f.write("No hay puntos registrados\n")
            else:
                for point in points:
                    name = point.get('Name', '')
                    f.write(f"- Punto: {name}\n")
                    participations = point.get('Participations', [])
                    if not participations:
                        f.write("No hay participantes registrados\n")
                    else:
                        participantes = set()
                        for participation in participations:
                            participante = participation.get('Participante', '')
                            if participante not in participantes:
                                participantes.add(participante)
                                f.write(f"  - {participante}:\n")
                            text = participation.get('text', '')
                            f.write(f"    {text}\n")
                    f.write("\n")
            f.write("\n")
    
    mostrar_documento_tkinter()
