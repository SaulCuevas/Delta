from PIL import Image, ImageOps, ImageDraw, ImageFont
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext
import gerber

from tkinter.filedialog import askdirectory
from glob import glob
import os
from VisionArtificial.PCB import interprete_gerber

path = askdirectory(title='Abrir carpeta con archivo GKO')
path_gko = os.path.normpath(glob(os.path.join(path, '**/*.GKO'), recursive=True)[0])
GKO = gerber.read(path_gko)
max_x = GKO.bounds[0][1]
# max_y = GKO.bounds[1][1]

top_bottom = input('¿Es top layer? (Y/N) ')

if top_bottom == 'Y' or top_bottom == 'y':
    _top_bottom = True
elif top_bottom == 'N' or top_bottom == 'n':
    _top_bottom = False
else:
    print('...')
    exit()

componentes_lista = interprete_gerber.obtener_pnp(path, _top_bottom)
for componente in componentes_lista:
    componente.x = (componente.x - max_x)*-1