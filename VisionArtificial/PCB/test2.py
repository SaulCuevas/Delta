import sys
import os
from glob import glob

from PIL import Image, ImageOps
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext

from tkinter.filedialog import askopenfilename, askdirectory

def putstr(text):
    sys.stdout.write(text)
    sys.stdout.flush()

path = askdirectory(title='Selecciona la carpeta CAM', initialdir='C:/Users/saulc/Documents/EAGLE/projects')

outline = load_layer(os.path.normpath(glob(os.path.join(path, '**/*.GKO'), recursive=True)[0]))
putstr('loading ')
copper = load_layer(os.path.normpath(glob(os.path.join(path, '**/*.GTL'), recursive=True)[0]))
putstr('.')
mask = load_layer(os.path.normpath(glob(os.path.join(path, '**/*.GTS'), recursive=True)[0]))
putstr('.')
silk = load_layer(os.path.normpath(glob(os.path.join(path, '**/*.GTO'), recursive=True)[0]))
putstr('.')
drill = load_layer(os.path.normpath(glob(os.path.join(path, '**/*.DRL'), recursive=True)[0]))
putstr('.')

ctx = GerberCairoContext(scale=20)
ctx.render_layer(outline)
putstr('.')

metal_settings = RenderSettings(color=(30.0 / 255.0, 119.0 / 255.0, 93 / 255.0))
bg_settings = RenderSettings(color=(30.0 / 300.0, 110.0 / 300.0, 93 / 300.0))
ctx.render_layer(copper, settings=metal_settings, bgsettings=bg_settings)
putstr('.')

copper_settings = RenderSettings(color=(0.9 * 1.2, 0.5 * 1.2, 0.1 * 1.2))
ctx.render_layer(mask, settings=copper_settings)
putstr('.')

our_settings = RenderSettings(color=theme.COLORS['white'], alpha=0.80)
ctx.render_layer(silk, settings=our_settings)
putstr('.')

ctx.render_layer(outline)
putstr('.')
ctx.render_layer(drill)
putstr('. end\n')
ctx.dump('Vision Artificial/PCB/board-top.png')