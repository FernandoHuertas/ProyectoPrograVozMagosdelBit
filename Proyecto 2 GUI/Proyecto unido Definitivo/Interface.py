
from tkinter import Button,Entry,Tk,messagebox,ttk,Toplevel, Menu, filedialog, Label, Listbox
from logic import section_creation, point_creation, generate_table_points,edit_section,delete_section, edit_point,delete_point, show_point, tablepart, agregar_participacion, add_person, delete_person, clear_list, save_list,show_agend, show_parts, open_data, generar_archivo_texto
from file_management import save
from pydub import AudioSegment
import speech_recognition as sr
from pydub.silence import split_on_silence
from pathlib import Path
from PIL import ImageTk, Image
from tkinter import messagebox, Menu, Entry

def get_value(box: Entry) -> str:
    """
    Obtiene el valor contenido en un cuadro de entrada.

    Args:
        box (Entry): Cuadro de entrada.

    Returns:
        str: Valor contenido en el cuadro de entrada.
    """
    return box.get()

def obtener_item(event, table):
    """
    Obtiene los valores de un elemento seleccionado en una tabla.

    Args:
        event: Evento que activa la función.
        table: Tabla en la que se encuentra el elemento.

    Returns:
        item_values: Valores del elemento seleccionado.
    """
    item_id = table.focus()
    item_values = table.item(item_id)["values"]
    return item_values

def volver_a_ventana_principal(win, winat):
    """
    Cierra la ventana actual y vuelve a la ventana principal.

    Args:
        win: Ventana actual.
        winat: Ventana principal.

    Returns:
        None
    """
    win.destroy()
    winat.deiconify()

def messages():
    """
    Muestra un cuadro de diálogo de confirmación.

    Returns:
        bool: True si se selecciona "yes", False si se selecciona "no".
    """
    result = messagebox.askquestion("Confirmacion", "¿Desea agregar otro punto dentro del apartado?")
    if result == "yes":
        return True
    else:
        return False

def on_table_double_click(event, table, points):
    """
    Acción a realizar al hacer doble clic en un elemento de la tabla.

    Args:
        event: Evento que activa la función.
        table: Tabla en la que se encuentra el elemento.
        points: Tabla de puntos asociada.

    Returns:
        None
    """
    item_id = table.focus()
    item_values = table.item(item_id)["values"]
    points.place(x=450, y=30)
    generate_table_points(points, item_values[0])

def show_context_menu(event, table):
    """
    Muestra un menú contextual al hacer clic derecho en un elemento de la tabla.

    Args:
        event: Evento que activa la función.
        table: Tabla en la que se encuentra el elemento.

    Returns:
        None
    """
    item_id = table.identify_row(event.y)
    if item_id:
        table.selection_set(item_id)
        menu = Menu(table, tearoff=0)
        menu.add_command(label="Editar", command=lambda: edit_section(table, item_id))
        menu.add_command(label="Eliminar", command=lambda: delete_section(table, item_id))
        menu.post(event.x_root, event.y_root)

def show_context_menu_point(event, table):
    """
    Muestra un menú contextual al hacer clic derecho en un elemento de la tabla de puntos.

    Args:
        event: Evento que activa la función.
        table: Tabla en la que se encuentra el elemento.

    Returns:
        None
    """
    item_id = table.identify_row(event.y)
    if item_id:
        table.selection_set(item_id)
        menu = Menu(table, tearoff=0)
        menu.add_command(label="Editar", command=lambda: edit_point(table, item_id))
        menu.add_command(label="Eliminar", command=lambda: delete_point(table, item_id))
        menu.post(event.x_root, event.y_root)


def Agend():
    """
    Función para gestionar la agenda.

    Returns:
        None
    """
    global style

    # Crear ventana de la agenda
    principal_window.withdraw()
    window_agend = Toplevel()
    
    window_agend.iconbitmap("Imagenes/Agenda.ico")
    

    # Crear tabla para los apartados
    table_agend = ttk.Treeview(window_agend, columns=("Apartado"), show="headings")
    table_agend.heading("Apartado", text="Apartado")

    # Crear tabla para los puntos
    table_point = ttk.Treeview(window_agend, columns=("Puntos"), show="headings")
    table_point.heading("Puntos", text="Puntos")

    # Cuadros de entrada para apartados y puntos
    txt_box_secction = Entry(window_agend, width=20, font=style)
    txt_box_point = Entry(window_agend, width=20, font=style)

    # Botones para agregar apartados y puntos
    btn_add_section = Button(window_agend, text="Agregar Apartado", width=15, height=1, font=style,
                             command=lambda: section_creation(get_value(txt_box_secction), btn_add_section,
                                                             btn_add_point, txt_box_secction))
    btn_add_point = Button(window_agend, text="Agregar Punto", width=15, height=1, font=style,
                           command=lambda: point_creation(get_value(txt_box_point), messages(), btn_add_section,
                                                         btn_add_point, txt_box_point, table_agend))

    # Etiqueta de instrucciones
    instruccion_agend = Label(window_agend,
                              text="Agregue los aprtados y puntos requeridos\n\nPara ver los puntos haga doble click sobre el Apartado\n\nPara editar o eliminar algun valor de click derecho sobre el")

    # Ubicación de los elementos en la ventana
    btn_add_section.pack(side="top", anchor="nw", pady=25, padx=45)
    txt_box_secction.pack(side="top", anchor="nw", pady=10, padx=20)
    btn_add_point.pack(side="top", anchor="nw", pady=25, padx=45)
    txt_box_point.pack(side="top", anchor="nw", pady=10, padx=20)
    table_agend.place(x=250, y=30)
    instruccion_agend.place(x=50, y=300)

    # Configuración de los elementos
    btn_add_point.config(state="disabled")
    window_agend.geometry("700x400")
    table_point.bind("<Button-3>", lambda event: show_context_menu_point(event, table_point))
    table_agend.bind("<Double-1>", lambda event: on_table_double_click(event, table_agend, table_point))
    table_agend.bind("<Button-3>", lambda event: show_context_menu(event, table_agend))

    # Mostrar la agenda
    show_agend(table_agend)
    btn_part.config(state="normal")

    window_agend.title("Agend")
    window_agend.protocol("WM_DELETE_WINDOW", lambda: volver_a_ventana_principal(window_agend, principal_window))

def aud():
    

    # Objetos visuales Tkinter declarados globalmente
    ruta_grabacion_a_dividir = None
    ruta_carpeta = None
    ruta_grabacion_a_reconocer = None
    resultado = None

    # Evento para el botón de iniciar la división del archivo
    def dividir():
        # Duración mínima de la pausa en milisegundos
        min_silence_len = 3000
        archivo_de_audio = ruta_grabacion_a_dividir.get()
        carpeta_de_segmentos = ruta_carpeta.get()
        audio_file = AudioSegment.from_wav(archivo_de_audio)

        audio_chunks = split_on_silence(
            audio_file,
            min_silence_len=min_silence_len,
            silence_thresh=-50
        )

        for i, chunk in enumerate(audio_chunks):
            print(f'Recorte número {i} procesado')
            chunk.export(f'{carpeta_de_segmentos}/grabacion_{i}.wav', format='wav')

        # Lanza un messagebox al finalizar las divisiones del audio
        messagebox.showinfo(
            "Fin del proceso de división",
            f"Se han terminado de procesar el archivo de audio, puede visualizar el resultado en la carpeta: {carpeta_de_segmentos}"
        )
        

    # Evento para el botón que selecciona el archivo a dividir
    def dialogo_grabacion():
        # Creamos el diálogo de selección de archivo
        filename = filedialog.askopenfilename(parent=window, title="Seleccione un archivo")

        # Si el usuario selecciona un archivo, mostramos la ruta en un Entry
        if filename:
            ruta_grabacion_a_dividir.delete(0, 'end')
            ruta_grabacion_a_dividir.insert('end', filename)
            btn_seleccionar_carpeta.config(state="normal")

    # Evento para el botón que selecciona la carpeta para almacenar los segmentos de grabaciones
    def dialogo_carpeta():
        # Creamos el diálogo de selección de carpeta
        directory = filedialog.askdirectory(parent=window, title="Seleccione una carpeta")

        # Si el usuario selecciona una carpeta, mostramos la ruta en un Entry
        if directory:
            ruta_carpeta.delete(0, 'end')
            ruta_carpeta.insert('end', directory)
            btn_dividir.config(state="normal")

    # Evento para el botón que selecciona el archivo a reconocer
    def dialogo_grabacion_reconocer():
        # Creamos el diálogo de selección de archivo
        filename = filedialog.askopenfilename(parent=window, title="Seleccione el archivo a reconocer")

        # Si el usuario selecciona un archivo, mostramos la ruta en un Entry
        if filename:
            ruta_grabacion_a_reconocer.delete(0, 'end')
            ruta_grabacion_a_reconocer.insert('end', filename)
            btn_reconocer.config(state="normal")

    # Evento para el botón que inicia el reconocimiento del texto
    def reconocer_texto(window):
        r = sr.Recognizer()
        try:
            with sr.AudioFile(ruta_grabacion_a_reconocer.get()) as source:
                audio_data = r.record(source)

            text = r.recognize_google(audio_data, language='es-ES')
            print(text)
            asig_texto(text, window)
            resultado.delete(0, 'end')
            resultado.insert('end', text)
            archivo_a_eliminar = ruta_grabacion_a_reconocer.get()
            path_archivo = Path(archivo_a_eliminar)
            path_archivo.unlink()
        except:
            messagebox.showinfo("Alerta","Direccion no valida")
    # Crear la ventana principal
    window = Tk()
    window.title("Divisor y reconocedor de audio")
    window.geometry("500x300")
    window.iconbitmap("Imagenes/correcto.ico")

    # Etiqueta y entrada para el archivo de audio a dividir
    lbl_archivo_dividir = Label(window, text="Archivo de audio a dividir:")
    lbl_archivo_dividir.pack()
    ruta_grabacion_a_dividir = Entry(window, width=50)
    ruta_grabacion_a_dividir.pack()

    # Botón para seleccionar el archivo a dividir
    btn_seleccionar_dividir = Button(window, text="Seleccionar", command=dialogo_grabacion)
    btn_seleccionar_dividir.pack()

    # Etiqueta y entrada para la carpeta de segmentos de grabaciones
    lbl_carpeta_segmentos = Label(window, text="Carpeta para segmentos de grabaciones:")
    lbl_carpeta_segmentos.pack()
    ruta_carpeta = Entry(window, width=50)
    ruta_carpeta.pack()

    # Botón para seleccionar la carpeta
    btn_seleccionar_carpeta = Button(window, text="Seleccionar", command=dialogo_carpeta)
    btn_seleccionar_carpeta.pack()
    btn_seleccionar_carpeta.config(state="disabled")

    # Botón para iniciar la división del archivo
    btn_dividir = Button(window, text="Dividir", command=dividir)
    btn_dividir.pack()
    btn_dividir.config(state="disabled")

    # Etiqueta y entrada para el archivo de audio a reconocer
    lbl_archivo_reconocer = Label(window, text="Archivo de audio a reconocer:")
    lbl_archivo_reconocer.pack()
    ruta_grabacion_a_reconocer = Entry(window, width=50)
    ruta_grabacion_a_reconocer.pack()

    # Botón para seleccionar el archivo a reconocer
    btn_seleccionar_reconocer = Button(window, text="Seleccionar", command=dialogo_grabacion_reconocer)
    btn_seleccionar_reconocer.pack()

    # Botón para iniciar el reconocimiento del texto
    btn_reconocer = Button(window, text="Reconocer texto", command=lambda:reconocer_texto(window))
    btn_reconocer.pack()
    btn_reconocer.config(state="disabled")

    # Etiqueta y entrada para mostrar el resultado del reconocimiento
    lbl_resultado = Label(window, text="Resultado:")
    lbl_resultado.pack()
    resultado = Entry(window, width=50)
    resultado.pack()

    # Ejecutar el bucle de eventos de la ventana
    principal_window.withdraw()
    window.protocol("WM_DELETE_WINDOW", lambda:volver_a_ventana_principal(window,principal_window))


def asig_texto(text, win):
    """
    Función para asignar texto a puntos y participantes seleccionados.

    Args:
        text (str): Texto a asignar.
        win (Tk): Ventana principal.

    Returns:
        None
    """
    win_asig = Toplevel()
    table_point = ttk.Treeview(win_asig, columns=("Puntos"), show="headings")
    table_point.heading("Puntos", text="Puntos")
    table_point.pack()
    table_part = ttk.Treeview(win_asig, columns=("Participantes"), show="headings")
    table_part.heading("Participantes", text="Participantes")
    table_part.pack()
    instruct = Label(win_asig, text="Haga doble clic sobre el punto\n y el participante al que desee añadir el texto\n despues presione confirmar")
    tablepart(table_part)
    show_point(table_point)
    point_value = None
    part_value = None

    # Función de callback para el doble clic en Puntos
    def on_point_double_click(event):
        nonlocal point_value
        item = table_point.identify_row(event.y)
        point = obtener_item(event, table_point)
        point_value = point

    # Función de callback para el doble clic en Participantes
    def on_part_double_click(event):
        nonlocal part_value
        item = table_part.identify_row(event.y)
        part = obtener_item(event, table_part)
        part_value = part
        btn_confirm.config(state="normal")

    def confirmar_part():
        agregar_participacion(point_value[0], text, part_value[0])
        volver_a_ventana_principal(win_asig, win)

    table_point.bind("<Double-1>", on_point_double_click)
    table_part.bind("<Double-1>", on_part_double_click)
    btn_confirm = Button(win_asig, text="Confirmar", command=confirmar_part)
    btn_confirm.pack()
    instruct.pack()
    btn_confirm.config(state="disabled")
    win_asig.geometry("300x600")
    win.withdraw()
    win_asig.protocol("WM_DELETE_WINDOW", lambda: volver_a_ventana_principal(win_asig, win))

def DEFCreateList_MainPopup():
    """
    Crea una ventana emergente para crear listas de personas.

    Permite agregar, eliminar, limpiar y guardar personas en una lista.

    Args:
        None

    Returns:
        None
    """
    global TextBox_WritePeopleName, listbox_ListofPeople
    MainpopupCreatelist = Toplevel()
    MainpopupCreatelist.geometry("400x300")
    MainpopupCreatelist.title("Crear listas menu") 

    MainpopupCreatelist.iconbitmap("Imagenes/iconoventana.ico")

    # Etiqueta para agregar personas
    label_EnterPeopleName = Label(MainpopupCreatelist, text="Introduzca el nombre de las personas:")
    label_EnterPeopleName.pack(pady=10)
    label_EnterPeopleName.place(x=25, y=25)
 
    # Caja de texto para agregar personas
    TextBox_WritePeopleName = Entry(MainpopupCreatelist)
    TextBox_WritePeopleName.pack(pady=5)
    TextBox_WritePeopleName.place(x=60, y=50)

    # Etiqueta para la lista de personas
    label_ListOfPeople = Label(MainpopupCreatelist, text="Lista de Personas:")
    label_ListOfPeople.pack(pady=10)
    label_ListOfPeople.place(x=70, y=75)

    # Lista de personas
    listbox_ListofPeople = Listbox(MainpopupCreatelist)
    listbox_ListofPeople.pack(pady=5)
    listbox_ListofPeople.place(x=60, y=100)

    # Botones de la ventana Crear lista
    # Botón para agregar personas
    button_add = Button(MainpopupCreatelist, text="Agregar", command=lambda: add_person(TextBox_WritePeopleName,listbox_ListofPeople))
    button_add.pack(pady=5)
    button_add.place(x=250, y=60)

    # Boton para eliminar cada personas seleccionada por el mouse
    button_deletePerson = Button(MainpopupCreatelist, text="Eliminar persona", command=lambda: delete_person(listbox_ListofPeople))
    button_deletePerson.pack(pady=7)
    button_deletePerson.place(x=250, y=100)

    # boton para limpiar toda la lista
    button_CleanList = Button(MainpopupCreatelist, text="Limpiar lista", command=lambda: clear_list(listbox_ListofPeople))
    button_CleanList.pack(pady=8)
    button_CleanList.place(x=250, y=140)

    # Botón para guardar la lista con un nombre
    button_SaveList = Button(MainpopupCreatelist, text="Guardar lista", command=lambda:save_list(listbox_ListofPeople))
    button_SaveList.pack(pady=9)
    button_SaveList.place(x=250, y=180)
    button_SaveList.bind('<Enter>', button_SaveList.config(bg='light blue')) #Color del boton

    show_parts(listbox_ListofPeople)

    btn_recon.config(state=("normal"))
    principal_window.withdraw()
    MainpopupCreatelist.protocol("WM_DELETE_WINDOW", lambda:volver_a_ventana_principal(MainpopupCreatelist,principal_window))


style=("Montserrat",13)
logo=None
#Objects
principal_window=Tk()
btn_agend=Button(text="Agenda", font=("Montserrat",16), command=Agend)
btn_recon=Button(text="Reconocimiento", font=("Montserrat",16), command=aud)
btn_part=Button(text="Participantes", font=("Montserrat",16), command=DEFCreateList_MainPopup)
btn_recon.config(state="disabled")
btn_part.config(state="disabled")
btn_save=Button(text="Guardar Reunion",font=("Montserrat",16), command=save)
btn_open=Button(text="Abrir Reunion existente",font=("Montserrat",16), command=lambda: open_data(btn_part, btn_recon))
btn_info=Button(text="Registro", font=("Montserrat",16), command=generar_archivo_texto)

imagen_l = Image.open("Imagenes/Logo.jpeg")
imagen_l=imagen_l.resize((250,250))
imagen_logo = ImageTk.PhotoImage(imagen_l)
logo = Label(principal_window, image=imagen_logo)



#Location
btn_agend.place(x=400, y=50)
btn_part.place(x=370, y=100)
btn_recon.place(x=355, y=150)
btn_save.place(x=352, y=200)
btn_open.place(x=325, y=250)
btn_info.place(x=380, y=300)
logo.place(x=20, y=50)

principal_window.iconbitmap("Imagenes/casas1.ico")
principal_window.geometry("600x380+300+0")
principal_window.config(bg="light blue")
principal_window.title("Sesiones de Organos colegiados")
principal_window.mainloop()