#Recursos nesesarios
import speech_recognition as sr
import datetime
import os

#Listas globales
lista_participantes=[]
lista_agenda=[]

def pedir_nombre():
    """
Esta funcion pide los nombres de la participantes y
 los agrega en la lista de participantes
junto con un numero como identificador de cada participante
    """
    global lista_participantes
    respuesta="Si"
    num=1
    while respuesta != "No":
        if respuesta=="Si":
            lista_participantes.append([])
            lista_participantes[-1].append(num)
            nombre=str(input("Introduzca el nombre completo del participante: "))
            while nombre == "":
                nombre=str(input("Introduzca el nombre completo del participante: "))
            lista_participantes[-1].append(nombre)
            num+=num
            respuesta=""
        respuesta=str(input("Desea agragar otro participante? (Responda con un Si o un No): "))
    return(lista_participantes)

def agenda():
    """
Crea la agenda Agregando sublistas en las que esta
el apartado y sus puntos correspondientes
    """
    global lista_agenda
    cont=1
    respuesta="Si"
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
            respuesta_puntos=str(input("Desea agragar otro punto dentro del apartado "+ apartado[0]+"? (Responda con un Si o un No): "))   
        limpiar()
        respuesta=str(input("Desea agragar otro apartado de agenda? (Responda con un Si o un No): "))
        apartado[1] = puntos
        if respuesta == "Si" or respuesta== "No":
            lista_agenda.append(apartado)

    return(lista_agenda)

def menu():
    """
    Imprime el menu de los apartados y puntos,
    recorriendo la lista agenda que esta anivel global
    """
    print("Agenda".center(50))
    global lista_agenda
    for elemento in lista_agenda:
        if elemento[0] and elemento != []:
            print("\n", elemento[0], "\n")
            if elemento[1]:
                for punto in elemento[1]:
                    print(punto[0], punto[1])

def menu_participantes():
    global lista_participantes
    for participante in lista_participantes:
        print(participante[0], participante[1])

def hora():
    hora_inicio = datetime.datetime.now()
    hora=[]
    hora.append(f"{hora_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    return(hora)

def grabacion(l:list):
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
                
                # Agregar la hora de inicio
                l[-1].append(hora())
        

                audio = r.listen(source)
                try:
                    text = r.recognize_google(audio, language='es-ES')
                    # Agregar texto reconocido
                    l[-1].append(text)
                except sr.UnknownValueError:
                    print("No se pudo entender lo que dijiste")
                except sr.RequestError as e:
                    print("No se pudo completar la solicitud: {0}".format(e))
            print(l)
        res=str(input("Desea seguir discutiendo este punto de agenda? (Responda con un Si o un No): "))

def limpiar():
    os.system("cls")

def transcripcion_grabacion():
    limpiar()
    agenda()
    limpiar()
    pedir_nombre()
    global lista_agenda,lista_participantes
    limpiar()
    com=""
    while com != "No":
        menu()
        try:
            com=int(input("\nSeleccione con el numero respectivo \nuno de los siguietes puntos de la Agenda: "))
        except:
            com=int(input("\nSeleccione con el numero respectivo \nuno de los siguietes puntos de la Agenda: "))
        limpiar()
        for x in lista_agenda:
            for e in x[1]:
                if e[0] == com:
                    grabacion(e[-1])
                    limpiar()
        limpiar()
        com=str(input("Desea tratar con otro punto de la agenda (Responda con un Si o un No): "))
        if com == "Si":
            pass
        elif com != "No":
            com=str(input("Desea tratar con otro punto de la agenda (Responda con un Si o un No): "))
        
    limpiar()



def imprimir_reporte1():
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


def cantidad_palabras_participante():
    global lista_participantes
    participantes=[]
    for par in lista_participantes:
        participantes.append([])
        participantes[-1].append(par[1])
        participantes[-1].append([])
    return (participantes)

def total_palabras():
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
    return(participantes)

def total_suma_palabras():
    suma=0
    palabras_totales=total_palabras()
    for longitud in palabras_totales:
        for s in longitud[1]:
            suma=suma+s
        longitud[1]=suma
        suma=0
    return palabras_totales
    
    
def imprimir_reporte2():
    palabras_totales=total_suma_palabras()
    obtener_valor_num(palabras_totales)
    palabras_totales = sorted(palabras_totales, key=obtener_valor_num, reverse=True)
    for palabras in palabras_totales:
        print(palabras[0]+": ",palabras[1])


def obtener_valor_num(sublista):
    for elem in sublista:
        if isinstance(elem, (float,int)):
            return elem
    return 0

def imprimir_reporte_3():
    """
Esta funcion imprime el reporte 3 el cual muestra el apartado con sus puntos dentro de el
y cuantas palabrasdijo capa persona en cada punto
    """
    global lista_agenda
    for x in lista_agenda:                                                      #Recorro la lista agenda para imprimir cada apartado 
        print("\n"+"\033[32m" + x[0].center(100) +"\033[0m")
        for e in x[1]:                                                          #Recorre los puntos de cada apartado
            cont=0                                                              #Se define el contador el cual reprecenta la la pocicion en la que estan cuantas palabras dijo la persona en cada apartado
            print("\n", e[0],"\033[31m"+ e[1].center(50) +"\033[0m"+"\n")       #Imprime el numero y el nombre de cada punto en el apartado
            participantes=total_palabras()                                      #Se aplica la funcion total_palabras
            for p in participantes:
                Lista_Participacion = []
                for i in e[2]:
                    if p[0] == i[0]:
                        Lista_Participacion.append(p[0])
                        Lista_Participacion.append(p[1][cont])
                if len(Lista_Participacion) > 1:
                    print(Lista_Participacion[0], " dijo en total ", Lista_Participacion[1],"palablras en el punto ",e[1])
                    cont+=1

def reportes():
    comando="Si"
    while comando !="No":
        if comando =="Si":
            limpiar()
            print("\n"+"REPORTES".center(30)+"\n")
            print("1. Este reporte dara todas los apartados con sus puntos\n y la participacion de cada parsona en cada punto")
            print("\n2. Este reporte dara la cantidad de palabras dichas\n por cada participante ordenado de mayor a menor")
            print("\n3. Este mostrara la cantidad de plabras dichas por los\n participantes en cada punto")
            comando=int(input("\nintrodusca un el numero del reporte que quiere ver: "))
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
                
transcripcion_grabacion()
reportes()
        
        







