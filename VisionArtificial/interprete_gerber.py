import os
from glob import glob
import csv
import math

from PIL import Image, ImageOps, ImageDraw, ImageFont
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext
import gerber

class componentes_class:
    def __init__(self, nombre : str, x : float, y : float, angulo : float, valor : str, paquete : str, numero : str) -> None:
        self.nombre = nombre
        self.x = float(x)
        self.y = float(y)
        self.angulo = float(angulo)
        self.valor = valor
        self.paquete = paquete
        self.numero = numero

class soldadura_class:
    def __init__(self, x, y, cantidad) -> None:
        self.x = x
        self.y = y
        self.cantidad = cantidad

def obtener_pnp(path : str, _top_bottom : bool):
    print("Leyendo archivo de componentes...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    fusion_kicad = False
    if _top_bottom:
        try:
            path_pnp = os.path.normpath(glob(os.path.join(path, '**/*top-pos.csv'), recursive=True)[0])
        except:
            try:
                fusion_kicad = True # No es Kicad 
                path_pnp = os.path.normpath(glob(os.path.join(path, '**/*front.csv'), recursive=True)[0])
            except:
                print("No existe tal archivo") # Convertir en mensaje de error en PyQt
    else:
        try:
            path_pnp = os.path.normpath(glob(os.path.join(path, '**/*bottom-pos.csv'), recursive=True)[0])
            if path_pnp == "": fusion_kicad = True # No es Kicad 
        except:
            try:
                fusion_kicad = True # No es Kicad 
                path_pnp = os.path.normpath(glob(os.path.join(path, '**/*back.csv'), recursive=True)[0])
            except:
                print("No existe tal archivo") # Convertir en mensaje de error en PyQt

    lista_componentes = []

    with open(path_pnp, 'r', newline='', encoding='ISO-8859-1') as csvfile:
        spamreader = csv.reader(csvfile)
        next(spamreader)
        it = 0
        for row in spamreader:
            if fusion_kicad:
                lista_componentes.append(componentes_class(row[0], row[1], row[2], row[3], row[4], row[5], it)) # parse para archivos fusion
            else:
                lista_componentes.append(componentes_class(row[0], row[3], row[4], row[5], row[1], row[2], it)) # parse para archivos kicad
            it += 1

    return lista_componentes

def obtener_soldadura(path : str, _top_bottom : bool):
    print("Leyendo archivo de soldadura...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    if _top_bottom == True:
        path_solder = os.path.normpath(glob(os.path.join(path, '**/*.GTP'), recursive=True)[0])
    else:
        path_solder = os.path.normpath(glob(os.path.join(path, '**/*.GBP'), recursive=True)[0])

    soldadura_lista = []

    copper = gerber.read(path_solder)
    for prim in copper.primitives:
        pos = (prim.bounding_box[0][0] + (prim.bounding_box[0][1] - prim.bounding_box[0][0]) / 2,
            prim.bounding_box[1][0] + (prim.bounding_box[1][1] - prim.bounding_box[1][0]) / 2)
        area_sqr = math.sqrt(math.sqrt(prim.bounding_box[0][1] - prim.bounding_box[0][0]) * (prim.bounding_box[1][1] - prim.bounding_box[1][0]))
        pulso = round(area_sqr, 3) # Se multiplica el area por un factor para convertir en segundos para el pulso de motor
        soldadura_lista.append(soldadura_class(round(pos[0], 4), round(pos[1], 4), pulso))
    return soldadura_lista

def limites_pcb(path : str):
    path_gko = os.path.normpath(glob(os.path.join(path, '**/*.GKO'), recursive=True)[0])
    GKO = gerber.read(path_gko)
    return GKO.bounds[0][1], GKO.bounds[1][1]

def mirror_bottom(path : str, componentes : componentes_class):
    max_x, _= limites_pcb(path)
    for componente in componentes:
        componente.x = (componente.x - max_x)*-1
    return componentes

def genImage(CAMFolder : str, top : bool):
    print("Cargando archivos de capa superior...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    copper = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTL'), recursive=True)[0]))
    mask = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTS'), recursive=True)[0]))
    silk = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTO'), recursive=True)[0]))
    drill = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.DRL'), recursive=True)[0]))
    try:
        outline = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GKO'), recursive=True)[0]))
    except:
        outline = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GM1'), recursive=True)[0]))

    print("Generando imagen de capa superior...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    ctx = GerberCairoContext(scale=20)

    metal_settings = RenderSettings(color=(30.0 / 255.0, 119.0 / 255.0, 93 / 255.0))
    bg_settings = RenderSettings(color=(30.0 / 300.0, 110.0 / 300.0, 93 / 300.0))
    ctx.render_layer(outline, settings=metal_settings, bgsettings=bg_settings)

    metal_settings = RenderSettings(color=(30.0 / 255.0, 119.0 / 255.0, 93 / 255.0))
    bg_settings = RenderSettings(color=(30.0 / 300.0, 110.0 / 300.0, 93 / 300.0))
    ctx.render_layer(copper, settings=metal_settings, bgsettings=bg_settings)

    copper_settings = RenderSettings(color=(0.9 * 1.2, 0.5 * 1.2, 0.1 * 1.2))
    ctx.render_layer(mask, settings=copper_settings)

    our_settings = RenderSettings(color=theme.COLORS['white'], alpha=0.80)
    ctx.render_layer(silk, settings=our_settings)

    ctx.render_layer(drill)

    ctx.dump('temp/board-top.png')

    ctx.clear()
    print("Cargando archivos de capa inferior...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    copper = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GBL'), recursive=True)[0]))
    mask = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GBS'), recursive=True)[0]))
    silk = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GBO'), recursive=True)[0]))

    print("Generando imagen de capa inferior") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    ctx.render_layer(outline, settings=metal_settings, bgsettings=bg_settings)
    ctx.render_layer(copper, settings=metal_settings, bgsettings=bg_settings)
    ctx.render_layer(mask, settings=copper_settings)
    ctx.render_layer(silk, settings=our_settings)
    ctx.render_layer(drill)

    ctx.dump('temp/board-bottom.png')

    im = Image.open('temp/board-bottom.png')
    im_mirror = ImageOps.mirror(im)
    im_mirror.save('temp/board-bottom.png', quality=100)

    print("Generando máscara para detección de PCB...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    if top:
        copper = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTL'), recursive=True)[0]))
        mask = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTS'), recursive=True)[0]))
        silk = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTO'), recursive=True)[0]))
        drill = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.DRL'), recursive=True)[0]))
        try:
            outline = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GKO'), recursive=True)[0]))
        except:
            outline = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GM1'), recursive=True)[0]))
        ctx.clear()
        metal_settings = RenderSettings(color=(255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0), mirror=False)
        bg_settings = RenderSettings(color=(0.0 / 300.0, 0.0 / 300.0, 0.0 / 300.0), mirror=False)
        ctx.render_layer(outline, settings=RenderSettings(color=(0, 0, 0)), bgsettings=bg_settings)
        ctx.render_layer(silk, settings=metal_settings, bgsettings=bg_settings)
        ctx.render_layer(mask, settings=metal_settings, bgsettings=bg_settings)
        ctx.render_layer(drill, settings=RenderSettings(mirror=False))

    else:
        ctx.clear()
        metal_settings = RenderSettings(color=(255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0), mirror=True)
        bg_settings = RenderSettings(color=(0.0 / 300.0, 0.0 / 300.0, 0.0 / 300.0), mirror=True)
        ctx.render_layer(outline, settings=RenderSettings(color=(0, 0, 0), mirror=True), bgsettings=bg_settings)
        ctx.render_layer(silk, settings=metal_settings, bgsettings=bg_settings)
        ctx.render_layer(mask, settings=metal_settings, bgsettings=bg_settings)
        ctx.render_layer(drill, settings=RenderSettings(mirror=True))
    ctx.dump('temp/board-mask.png')

def genImageList(CAMFolder : str, _top_bottom : bool):
    pnp = obtener_pnp(CAMFolder, _top_bottom)
    if(_top_bottom):
        img_path = "temp/board-top.png"
    else:
        img_path = "temp/board-bottom.png"
    img = Image.open(img_path)
    w , h = img.size
    I1 = ImageDraw.Draw(img)
    myFont = ImageFont.truetype('arial.ttf', 40)
    for componente in pnp:
        if(_top_bottom):
            bbox = I1.textbbox((float(componente.x)*20,h-float(componente.y)*20), str(componente.numero), font=myFont, anchor='mm')
            I1.rectangle(bbox, fill='white')
            I1.text((float(componente.x)*20,h-float(componente.y)*20), str(componente.numero), fill = 'red', font=myFont, anchor='mm')
        else:
            bbox = I1.textbbox((w-float(componente.x)*20,h-float(componente.y)*20), str(componente.numero), font=myFont, anchor='mm')
            I1.rectangle(bbox, fill='white')
            I1.text((w-float(componente.x)*20,h-float(componente.y)*20), str(componente.numero), fill = 'red', font=myFont, anchor='mm')
    
    img.save("temp/board-list.png")
