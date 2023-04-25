#Recursos nesesarios
import speech_recognition as sr
import datetime
import os

#Listas globales
lista_participantes=[]
lista_agenda=[]

def agenda():
    """_Creacion de Agenda_
            Crea la agenda Agregando sublistas en las que esta
            el apartado y sus puntos correspondientes.
    Returns:
            lista_agenda(list): _lista donde se agregan sublistas de los apartados,
            sus puntos con sus numero y un lista vacía para las participaciones_
    """
    #Crea minimo un apartado y un punto en la agenda que se agrega en la "lista_agenda" y preguntar si quiere agregar mas
    global lista_agenda
    cont=1
    #respuesta:str= Variable de entrada para indicar cuando agregar un apartado
    respuesta="Si"
    #respuesta_punto:str= Variable de entrada para indicar cuando agregar un punto
    respuesta_puntos=""
    while respuesta != "No":
        apartado=[]
        if respuesta=="Si":
                nombre_apartado=str(input("Agregue un apartado de agenda: "))
                while nombre_apartado =="":
                    nombre_apartado=str(input("Agregue un apartado de agenda: "))
                apartado.append(nombre_apartado)
                apartado.append([])
                respuesta_puntos="Si"
        puntos = []
        while respuesta_puntos != "No":
            if respuesta_puntos=="Si":
                punto=str(input("Agregue un punto dentro del apartado "+ apartado[0]+": "))
                while punto =="":
                    punto=str(input("Agregue un punto dentro del apartado "+ apartado[0]+": "))
                puntos.append([cont, punto, []])
                cont=cont+1
            limpiar()
            respuesta_puntos=str(input("Desea agregar otro punto dentro del apartado "+ apartado[0]+"? (Responda con un Si o un No): "))   
        limpiar()
        respuesta=str(input("Desea agregar otro apartado de agenda? (Responda con un Si o un No): "))
        while respuesta != "Si" and respuesta != "No":
            respuesta=str(input("Desea agregar otro apartado de agenda? (Responda con un Si o un No): "))
        apartado[1] = puntos
        lista_agenda.append(apartado)

    return(lista_agenda)

def pedir_nombre():
    """_Pededir Nombre_
        Crea una lista con los participantes y
        con un numero como identificador de cada participante

    Returns:
            lista_participantes(list): _lista donde se agregan sublistas con 
            el numero identificador y el nombre de cada participante_
    """
    global lista_participantes
    respuesta="Si"
    num=1
    while respuesta != "No":
        limpiar()
        if respuesta=="Si":
            lista_participantes.append([])
            lista_participantes[-1].append(num)
            nombre=str(input("Introduzca el nombre completo del participante: "))
            while nombre == "":
                nombre=str(input("Introduzca el nombre completo del participante: "))
            lista_participantes[-1].append(nombre)
            num+=1
            respuesta=""
        respuesta=str(input("Desea agragar otro participante? (Responda con un Si o un No): "))
    return(lista_participantes)

def menu():
    """_Imprime menu de Agenda_

            _Imprime los apartados y puntos
            recorriendo la lista_agenda que esta global_
    """
    print("\n"+"\033[35m" + "AGENDA".center(50) +"\033[0m")
    global lista_agenda
    for elemento in lista_agenda:
        if elemento[0] and elemento != []:
            print("\n"+"\033[32m" + elemento[0].center(25) +"\033[0m")
            if elemento[1]:
                for punto in elemento[1]:
                    print(punto[0], punto[1])

def menu_participantes():
    """_Imprime menu de Participantes_

            _Imprime el numero identificador y el nombre de cada participante
            recorriendo la lista_participantes que esta global_
    """
    global lista_participantes
    print("\n"+"\033[35m" + "PARTICIPANTES".center(50) +"\033[0m")
    for participante in lista_participantes:
        print(participante[0], participante[1])

def hora():
    """_Hora_
        _Consulta la hora actual del sistema y la agrega a una lista
        como un str indicando: año, mes, día, hora, minuto y segundo_
    Returns:
        hora(list): _lista donde se almacena la hora actual_
    """
    hora_inicio = datetime.datetime.now()
    hora=[]
    hora.append(f"{hora_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    return(hora)

def grabacion(l:list):
    """_Grabacion de voz_
        Graba lo que el participante dice,
        lo manda al servidor de google y el audio reconocido
        lo convierte a texto
    Args:
        l (list): _Lista donde se va a almacenar el texto reconocido del microfono 
        una vez que haya sido procesado_
    """
    r=sr.Recognizer()
    res="Si"
    while res !="No":
        if res=="Si":
            
            menu_participantes()
            try:
                num=int(input("Seleccione con el numero respectivo \nel participante que va a hablar: "))
            except:
                num=int(input("Seleccione con el numero respectivo \nel participante que va a hablar: "))
            for x in lista_participantes:
                if x[0]==num:
                    l.append([])
                    l[-1].append(x[1])
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)  
                print("Habla ahora...")
                
                # Agrega la hora de inicio
                l[-1].append(hora())
        

                audio = r.listen(source)
                try:
                    text = r.recognize_google(audio, language='es-ES')
                    # Agrega texto reconocido
                    l[-1].append(text)
                except sr.UnknownValueError:
                    print("No se pudo entender lo que dijiste")
                    l.remove(l[-1])
                except sr.RequestError as e:
                    print("No se pudo completar la solicitud: {0}".format(e))
                    l.remove(l[-1])
            for texto in l:
                print(texto)
        res=str(input("Desea seguir discutiendo este punto de agenda? (Responda con un Si o un No): "))

def limpiar():
    """_Limpia terminal_

        _Limpia la terminal de texto_
    """
    os.system("cls")

def Programa():
    """_Algoritmo principal_

        _Ejecuta cada funcion en un orden determinado para que el programa
        funcione correctamente y se muestre al usuario en la terminal_
    """
    limpiar()
    agenda()
    limpiar()
    pedir_nombre()
    global lista_agenda,lista_participantes
    limpiar()
    comando=""
    while comando != "No":
        menu()
        try:
            comando=int(input("\nSeleccione con el numero respectivo \nuno de los siguientes puntos de la Agenda: "))
        except:
            comando=int(input("\nSeleccione con el numero respectivo \nuno de los siguientes puntos de la Agenda: "))
        limpiar()
        for Apartados in lista_agenda:
            for Puntos in Apartados[1]:
                if Puntos[0] == comando:
                    grabacion(Puntos[-1])
                    limpiar()
        limpiar()
        comando=str(input("Desea tratar con otro punto de la agenda (Responda con un Si o un No): "))
        if comando == "Si":
            pass
        elif comando != "No":
            comando=str(input("Desea tratar con otro punto de la agenda (Responda con un Si o un No): "))
        
    limpiar()

def cantidad_palabras_participante():
    """_Crea lista con participantes_

    Returns:
        participantes(list): _Lista con sublistas que contienen el nombre del participante 
        y otra sublista vacia_
    """
    global lista_participantes
    participantes=[]
    for par in lista_participantes:
        participantes.append([])
        participantes[-1].append(par[1])
        participantes[-1].append([])
    return (participantes)

def total_palabras():
    """_Palabras de cada Participante_
        _Agrega la hora y todas las palabras que dice cada participante a la lista
        participantes_
    Returns:
        participantes(list): _Almacena sublistas con el nombre de cada participante y
        todas sus participaciones con su hora respectiva_
    """
    global lista_agenda
    palabras=[]
    participantes=cantidad_palabras_participante()
    for apartados in lista_agenda:
        
        for puntos in apartados[1]:
            for persona in lista_participantes:
                Lista_Participacion = []
                Lista_Participacion.append(persona[1])
                if persona[1] in [comversacion[0] for comversacion in puntos[2]]:
                    for comversacion in puntos[2]:
                        if persona[1]==comversacion[0]:
                            Lista_Participacion.append(comversacion[2])
                if len(Lista_Participacion) > 1:
                    participante = Lista_Participacion[0]
                    palabras_participante = ' '.join(Lista_Participacion[1:]).split()
                    palabras.extend(palabras_participante)
                    palabras_participante=len(palabras_participante)
                    for elementos in participantes:
                        if Lista_Participacion[0] == elementos[0]:
                            elementos[1].append(palabras_participante)
                else:
                    for elementos in participantes:
                        if Lista_Participacion[0] == elementos[0]:
                            elementos[1].append(0)

    return(participantes)

def total_suma_palabras():
    """_Cuenta de palabras_
        _Cuenta la cantidad de palabras que dijo cada participante_
    Returns:
        palabras_totales(list): _lista con el total depalabras que dijo cada persona_
    """
    suma=0
    palabras_totales=total_palabras()
    for longitud in palabras_totales:
        for s in longitud[1]:
            suma=suma+s
        longitud[1]=suma
        suma=0
    return palabras_totales

def imprimir_reporte1():
    """_Imprime el reporte 1_

        _Recorre las 2 listas golbales e imprime el aprtado, el punto, el participante y todas sus
        participaciones en su punto respectivo_
    """
    limpiar()
    global lista_agenda
    global lista_participantes
    for x in lista_agenda:
        print("\n"+"\033[31m" + x[0].center(100) +"\033[0m")
        for e in x[1]:
            print("\n", e[0],"\033[32m"+ e[1].center(50) +"\033[0m"+"\n")
            for p in lista_participantes:
                Lista_Participacion = []
                Lista_Participacion.append(p[1])
                for i in e[2]:
                    if p[1] == i[0]:
                        Lista_Participacion.append(i[1])
                        Lista_Participacion.append(i[2])
                if len(Lista_Participacion) > 1:
                    print(Lista_Participacion[0], ":")
                    for f in Lista_Participacion[1:]:
                        print(f)
    
def imprimir_reporte2():
    """_Imprime el reporte 2_
    
        _Recorre la lista palabras_totales 
        que contiene las palabras totales de cada participantes de mayor a menor 
        y lo imprime_
    """
    limpiar()
    palabras_totales=total_suma_palabras()
    obtener_valor_num(palabras_totales)
    palabras_totales = sorted(palabras_totales, key=obtener_valor_num, reverse=True)
    print("\n"+"TOTAL DE PALABRAS".center(100)+"\n")
    for palabras in palabras_totales:
        print(palabras[0]+": ",palabras[1])

def obtener_valor_num(sublista):
    """_Devuelve el numero de una sublista_

    Esta función busca el primer número (entero o decimal) en una sublista y devuelve ese valor.

    Args:
        sublista (list): La sublista en la que se buscará el número.

    Returns:
        float or int: El primer número encontrado en la sublista, o 0 si no se encuentra ningún número.
    """
    for elem in sublista:
        if isinstance(elem, (float,int)):
            return elem
    return 0

def imprimir_reporte_3():
    """_Imprime el reporte 3_

        _Imprime el reporte 3 el cual muestra el apartado con sus puntos dentro de el
        y cuantas palabras dijo capa persona en cada punto_
    """
    limpiar()
    global lista_agenda
    participantes=total_palabras()
    cont=0
    for x in lista_agenda:                                                      #Recorro la lista agenda para imprimir cada apartado 
        print("\n"+"\033[32m" + x[0].center(100) +"\033[0m")
        
        for e in x[1]:                                                          #Recorre los puntos de cada apartado                              
            print("\n", e[0],"\033[31m"+ e[1].center(50) +"\033[0m"+"\n")       #Imprime el numero y el nombre de cada punto en el apartado
                                                 
            for p in participantes:
                
                Lista_Participacion = []
                for i in e[2]:
                    if p[0] == i[0]:
                        Lista_Participacion.append(p[0])

                        Lista_Participacion.append(p[1][cont])
                        print(Lista_Participacion[0], " dijo en total ", Lista_Participacion[1],"palabras en el punto ",e[1])            
            cont+=1
def reportes():
    """_Seleccion de reportes_

        _Muestra una interfaz en terminal para que eliga cual de los 3 reportes quiere mostrar_
    """
    limpiar()

    comando="Si"
    while comando !="No":
        if comando =="Si":
            limpiar()
            print("\n"+"REPORTES".center(30)+"\n")
            print("1. \033[32mEste reporte dara todas los apartados con sus puntos\n y la participacion de cada parsona en cada punto\033[0m")
            print("\n2. \033[33mEste reporte dara la cantidad de palabras dichas\n por cada participante ordenado de mayor a menor\033[0m")
            print("\n3. \033[36mEste mostrara la cantidad de plabras dichas por los\n participantes en cada punto\033[0m")
            try:
                comando = int(input("\nIntroduzca un el numero del reporte que quiere "))
            except:
                print("Valor invalido")
            if comando == 1:
                imprimir_reporte1()
            elif comando ==2:
                imprimir_reporte2()
            elif comando ==3:
                imprimir_reporte_3()
            else:
                print("No valido")
                pass
            comando=str(input("\nDesea ver otro reporte (Responda con un Si o un No): "))
            while comando != "Si" and comando != "No":
                comando=str(input("\nDesea ver otro reporte (Responda con un Si o un No): "))
                
Programa()
reportes()