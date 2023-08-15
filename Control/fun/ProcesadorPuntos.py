# Ingresando un conjunto de puntos del tipo
# [ px, py, pz, tipo_de_movimiento, herramienta (opcional) ]
# para cada punto
# con tipo_de_movimiento:
#               * 'max_vel'     = 500 mm/s
#               * 'libre'       = 400 mm/s
#               * 'pick_place'  = 20 mm/s
#               * 'approach'    = 350 mm/s
#               * 'home'        = 250 mm/s
# con herramienta:
#               * 'cam'         = [x, y, z]
#               * 'soldadura'   = [x, y, z]
#               * 'pnp'         = [x, y, z]

import numpy as np

offset_cam = np.array([5.0, 6.0, 7.0])
offset_soldadura = np.array([5.0, 6.0, 7.0])
offset_pnp = np.array([5.0, 6.0, 7.0])

def offset(px, py, pz, herramienta : str):
    match herramienta:
        case 'cam':
            return px-offset_cam[0], py-offset_cam[1], pz-offset_cam[2]
        case 'soldadura':
            return px-offset_soldadura[0], py-offset_soldadura[1], pz-offset_soldadura[2]
        case 'pnp':
            return px-offset_pnp[0], py-offset_pnp[1], pz-offset_pnp[2]