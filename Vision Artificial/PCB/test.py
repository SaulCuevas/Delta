import interprete_gerber

from tkinter.filedialog import askdirectory

class soldadura_class:
    def __init__(self, x, y, cantidad) -> None:
        self.x = x
        self.y = y
        self.cantidad = cantidad

path = askdirectory(title='Abrir carpeta con archivo de soldadura')

top_bottom = input('¿Es top layer? (Y/N) ')

if top_bottom == 'Y' or top_bottom == 'y':
     _top_bottom = True
elif top_bottom == 'N' or top_bottom == 'n':
     _top_bottom = False
else: print('...')

soldadura_lista = interprete_gerber.obtener_soldadura(path, _top_bottom)
componentes_lista = interprete_gerber.obtener_pnp(path, _top_bottom)
interprete_gerber.genImage(path, _top_bottom)

for x in soldadura_lista:
    print(x.x, x.y, x.cantidad)

print("__________________________________________")

for x in componentes_lista:
    print(x.numero, x.nombre, x.x, x.y, x.angulo, x.valor, x.paquete)

interprete_gerber.genImageList(path, _top_bottom)