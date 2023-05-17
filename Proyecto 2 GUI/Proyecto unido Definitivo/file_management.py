from logic import Agend, lista_participantes
from tkinter.filedialog import asksaveasfile
def save():
    global Agend, lista_participantes
    file = asksaveasfile(defaultextension=".txt")
    if file is None:
        return
    filename = file.name
    with open(filename, 'w') as f:
        f.write(str(Agend) + '\n')
        f.write(str(lista_participantes))
    file.close()


