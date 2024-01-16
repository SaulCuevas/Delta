import cv2
import numpy as np
import math

pixeles_por_mm = 42.3216
pos_disco = [45.00, -65.00, 187.00] 

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def genMaskSMD(img, h, w):
    mask = np.zeros((h,w,1), np.uint8)
    cv2.circle(mask, [w,h], h, 255, -1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (45,45), 0)
    # hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

    color_pcb = int(200/2)

    # Eliminar el color del disco
    lower = np.array([90, int(0/100 * 255), int(40/100 * 255)])
    upper = np.array([120, int(100/100 * 255), int(100/100 * 255)])
    mask_SMD_2 = cv2.inRange(hsv, lower, upper)
    mask_SMD_2 = cv2.bitwise_not(mask_SMD_2)
    mask_SMD_2 = cv2.bitwise_and(mask_SMD_2, mask)

    # # Eliminar el color del disco
    # lower = np.array([90, int(0/100 * 255), int(35/100 * 255)])
    # upper = np.array([120, int(100/100 * 255), int(100/100 * 255)])
    # mask_SMD_2 = cv2.inRange(hsv, lower, upper)
    # mask_SMD_2 = cv2.bitwise_not(mask_SMD_2)
    # mask_SMD_2 = cv2.bitwise_and(mask_SMD_2, mask)

    hsv = cv2.GaussianBlur(hsv, (111,111), 0)

    # Eliminar zonas oscuras
    lower = np.array([0, int(0/100 * 255), int(50/100 * 255)])
    upper = np.array([180, int(100/100 * 255), int(100/100 * 255)])
    mask_SMD = cv2.inRange(hsv, lower, upper)
    mask_SMD = cv2.bitwise_and(cv2.bitwise_not(mask_SMD), mask)

    # # Eliminar zonas oscuras
    # lower = np.array([0, int(0/100 * 255), int(50/100 * 255)])
    # upper = np.array([180, int(100/100 * 255), int(100/100 * 255)])
    # mask_SMD = cv2.inRange(hsv, lower, upper)
    # mask_SMD = cv2.bitwise_and(cv2.bitwise_not(mask_SMD), mask)

    # Taking a matrix of size 5 as the kernel 
    # kernel = np.ones((3, 3), np.uint8) 
    # mask_SMD_2 = cv2.erode(mask_SMD_2, kernel)
    kernel = np.ones((17, 17), np.uint8) 
    mask_SMD = cv2.erode(mask_SMD, kernel)

    # cv2.imshow("smd", ResizeWithAspectRatio(mask_SMD, height=960))
    # cv2.imshow("smd2", ResizeWithAspectRatio(mask_SMD_2, height=960))

    mask_SMD = mask_SMD + mask_SMD_2
    kernel = np.ones((31, 31), np.uint8) 
    mask_SMD = cv2.dilate(mask_SMD, kernel)
    mask_SMD = cv2.erode(mask_SMD, kernel)

    # cv2.imshow("res", ResizeWithAspectRatio(mask_SMD, height=960))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return mask, mask_SMD

def genMaskTriang(mask_in, h, w):
    points = np.array([[int(w-w/20), h], [w, 0], [int(w-w/20 - h*math.tan(math.radians(26))), 0]])
    mask_r1 = np.zeros((h,w,1), np.uint8)
    cv2.fillPoly(mask_r1, pts=[points], color=(255, 255, 255))
    mask_r1 = cv2.bitwise_and(mask_r1, mask_in)

    points = np.array([[int(w-w/20), h], [int(w-w/20 - h*math.tan(math.radians(26))), 0], [0, int(h-w*math.tan(math.radians(31)))]])
    mask_r2 = np.zeros((h,w,1), np.uint8)
    cv2.fillPoly(mask_r2, pts=[points], color=(255, 255, 255))
    mask_r2 = cv2.bitwise_and(mask_r2, mask_in)

    points = np.array([[int(w-w/20), h], [0, int(h-w*math.tan(math.radians(31)))], [0, int(h-w*math.tan(math.radians(1)))]])
    mask_r3 = np.zeros((h,w,1), np.uint8)
    cv2.fillPoly(mask_r3, pts=[points], color=(255, 255, 255))
    mask_r3 = cv2.bitwise_and(mask_r3, mask_in)

    return mask_r1, mask_r2, mask_r3

def getSortedContours(img, mask_r1, mask_r2, mask_r3, mask_SMD, w, h):
    cnts_cuadrante = []
    centroid_cuadrante = []
    angle_cuadrante = []

    for x in range(3):
        if(x == 0):
            mask_cuadrante = cv2.bitwise_and(mask_r1, mask_SMD)
        elif(x == 1):
            mask_cuadrante = cv2.bitwise_and(mask_r2, mask_SMD)
        else:
            mask_cuadrante = cv2.bitwise_and(mask_r3, mask_SMD)
        # Gaussian Blur
        blur = cv2.GaussianBlur(mask_cuadrante, (3,3), 0)

        # Find Canny edges 
        edged = cv2.Canny(mask_cuadrante, 30, 200) 
        
        # Finding Contours 
        # Use a copy of the image e.g. edged.copy() 
        # since findContours alters the image 
        contours, _ = cv2.findContours(edged,  
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

        cnts_filtrados = []
        for cnt in contours:
            if(cv2.arcLength(cnt,True))>40:
                cnts_filtrados.append(cnt)

        contours = cnts_filtrados

        cnts_filtrados = []
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            cnts_filtrados.append(box)

        # print("Number of Contours found = " + str(len(cnts_filtrados))) 
        if( len(cnts_filtrados) == 0 ):
            continue

        # Draw all contours 
        # -1 signifies drawing all contours 
        cv2.drawContours(img, cnts_filtrados, -1, (0, 255, 0), 3)
        radius = 0
        radius_array = []
        centroid_array = []
        angle_array = []

        for cnt in cnts_filtrados:
            esq_izq = cnt[0]
            esq_sup = cnt[1]
            esq_inf = cnt[3]
            long_V = math.sqrt( (esq_izq[0] - esq_sup[0])**2 + (esq_izq[1] - esq_sup[1])**2 )
            long_H = math.sqrt( (esq_izq[0] - esq_inf[0])**2 + (esq_izq[1] - esq_inf[1])**2 )
            centroid = [int((cnt[2][0] - cnt[0][0])/2 + cnt[0][0]), int((cnt[2][1] - cnt[0][1])/2 + cnt[0][1])]
            if( long_H < long_V ):
                angle = math.atan2(esq_sup[1]-esq_izq[1], esq_izq[0]-esq_sup[0])
            else:
                angle = math.atan2(esq_inf[1]-esq_izq[1], esq_izq[0]-esq_inf[0])
            
            if(angle>math.pi/2):
                angle -= math.pi/2
                angle = math.pi/2 - angle
            if(angle<-math.pi/2):
                angle += math.pi/2
                angle = -1*(math.pi/2 + angle)
            
            angle = math.degrees(angle)

            radius = int(math.sqrt( (w - centroid[0])**2 + (h - centroid[1])**2 )/50)
            radius_array.append(radius)
            centroid_array.append(centroid)
            angle_array.append(angle)

        sort = np.argsort(radius_array)
        radius_array = np.sort(radius_array)

        cnts_por_radio = []
        centroid_por_radio = []
        angle_por_radio = []

        for x in sort:
            cnts_por_radio.append(cnts_filtrados[x])
            centroid_por_radio.append(centroid_array[x])
            angle_por_radio.append(angle_array[x])

        mem = []
        new_sort = []
        cont = 0
        start_index = 0

        for index in range(len(radius_array)):
            # En radios lejanos (>+1) (<-1), iniciar una memoria de arreglo nueva
            # ordenar la lista guardada y generar o agregar el indice de orden
            if((index>0) and ( radius_array[index-1] < (radius_array[index]-1) )):
                cont += 1
                temp_sort = np.argsort(mem) + start_index
                temp_sort = temp_sort[::-1]
                # print(cont, temp_sort)
                new_sort.extend(temp_sort)
                mem.clear()
                # print(str(cont) + ": fila++")
                mem.append(centroid_por_radio[index][0])
                start_index = index
            # En radios cercanos agregar el radio actual a una lista
            else:
                # print(str(cont) + ": fila==")
                mem.append(centroid_por_radio[index][0])
            if(index == len(radius_array)-1):
                cont += 1
                temp_sort = np.argsort(mem) + start_index
                temp_sort = temp_sort[::-1]
                # print(cont, temp_sort)
                new_sort.extend(temp_sort)
                mem.clear()
                # print(str(cont) + ": fila++")
        
        for x in new_sort:
            cnts_cuadrante.append(cnts_por_radio[x])
            centroid_cuadrante.append(centroid_por_radio[x])
            angle_cuadrante.append(angle_por_radio[x])

    return cnts_cuadrante, centroid_cuadrante, angle_cuadrante

def getCentroidAngleSMD(path1, path2, path3, path4):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    img3 = cv2.imread(path3)
    img4 = cv2.imread(path4)
    cnts_finales = []
    centroid_finales = []
    angle_finales = []

    for y in range(4):
        match y:
            case 0:
                img = img1
            case 1:
                img = img2
            case 2:
                img = img3
            case 3:
                img = img4
                
        [h, w, _] = img.shape
        mask, mask_SMD = genMaskSMD(img, h, w)

        # cv2.imshow('mask_SMD', ResizeWithAspectRatio(mask_SMD, height=960)) 

        mask_r1, mask_r2, mask_r3 = genMaskTriang(mask, h, w)

        cnts_cuadrante, centroid_cuadrante, angle_cuadrante = getSortedContours(img, mask_r1, mask_r2, mask_r3, mask_SMD, w, h)

        for x in range(len(cnts_cuadrante)):
            cv2.circle(img, [cnts_cuadrante[x][0][0], cnts_cuadrante[x][0][1]], 10, [255, 0, 0], -1)
            cv2.circle(img, [cnts_cuadrante[x][1][0], cnts_cuadrante[x][1][1]], 10, [0, 255, 0], -1)
            cv2.circle(img, [cnts_cuadrante[x][2][0], cnts_cuadrante[x][2][1]], 10, [0, 0, 255], -1)
            cv2.circle(img, [cnts_cuadrante[x][3][0], cnts_cuadrante[x][3][1]], 10, [255, 255, 0], -1)
            cv2.circle(img, centroid_cuadrante[x], 10, [255, 0, 255], -1)
            cv2.putText(img, str(x+1 + y*54), centroid_cuadrante[x], cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 4, cv2.LINE_AA)
            cnts_finales.append(cnts_cuadrante[x])
            centroid_finales.append(centroid_cuadrante[x])
            angle_finales.append(angle_cuadrante[x])

        # cv2.imshow('Contours', ResizeWithAspectRatio(img, height=960))
        # cv2.waitKey(0) 
        # cv2.destroyAllWindows() 
        
        match y:
            case 0:
                new_img1 = img
            case 1:
                new_img2 = img
            case 2:
                new_img3 = img
            case 3:
                new_img4 = img

    for centroide in centroid_finales:
        centroide[0] = centroide[0]-w/2 # offset en x desde el centro de la imagen
        centroide[1] = h/2-centroide[1] # offset en y desde el centro de la imagen

        centroide[0] = centroide[0]/pixeles_por_mm
        centroide[1] = centroide[1]/pixeles_por_mm

        centroide[0] += pos_disco[0]
        centroide[1] += pos_disco[1]
    
    return new_img1, new_img2, new_img3, new_img4, centroid_finales, angle_finales
