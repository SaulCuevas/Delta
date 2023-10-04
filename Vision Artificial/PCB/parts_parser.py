import os
from glob import glob
from tkinter.filedialog import askdirectory
import csv

class componentes_class:
    def __init__(self, nombre, x, y, angulo, valor, paquete) -> None:
        self.nombre = nombre
        self.x = x
        self.y = y
        self.angulo = angulo
        self.valor = valor
        self.paquete = paquete

def parse_pnp(path, _top_bottom):
    fusion_kicad = False
    if _top_bottom == 'Y' or _top_bottom == 'y':
        try:
            path_pnp = os.path.normpath(glob(os.path.join(path, '**/*top-pos.csv'), recursive=True)[0])
        except:
            try:
                fusion_kicad = True # No es Kicad 
                path_pnp = os.path.normpath(glob(os.path.join(path, '**/*front.csv'), recursive=True)[0])
            except:
                print("No existe tal archivo")
    elif _top_bottom == 'N' or _top_bottom == 'n':
        try:
            path_pnp = os.path.normpath(glob(os.path.join(path, '**/*bottom-pos.csv'), recursive=True)[0])
            if path_pnp == "": fusion_kicad = True # No es Kicad 
        except:
            try:
                fusion_kicad = True # No es Kicad 
                path_pnp = os.path.normpath(glob(os.path.join(path, '**/*back.csv'), recursive=True)[0])
            except:
                print("No existe tal archivo")
    else:
        print('...')

    lista_componentes = []

    with open(path_pnp, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if fusion_kicad:
                lista_componentes.append(componentes_class(row[0], row[1], row[2], row[3], row[4], row[5])) # parse para archivos fusion
            else:
                lista_componentes.append(componentes_class(row[0], row[3], row[4], row[5], row[1], row[2])) # parse para archivos kicad

    lista_componentes.pop(0)

    return lista_componentes

path = askdirectory(title='Abrir carpeta con PnP (Top/Bottom)')

top_bottom = input('¿Es top layer? (Y/N) ')

componentes_pnp = parse_pnp(path, top_bottom)

for x in componentes_pnp:
    print(x.nombre, x.x, x.y, x.angulo, x.valor, x.paquete)