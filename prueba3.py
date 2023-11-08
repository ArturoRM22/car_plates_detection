import cv2
import pytesseract
import random

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

image_files = ['auto001.jpg', 'auto003.png', 'auto007.jpeg', 'auto009.jpg'] 

random_image = random.choice(image_files)

placa = []
image = cv2.imread(random_image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray, (3, 3))
canny = cv2.Canny(gray, 150, 200)
canny = cv2.dilate(canny, None, iterations=1)

cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, cnts, -1, (0, 225, 0), 2)

for c in cnts:
    area = cv2.contourArea(c)
    x, y, w, h = cv2.boundingRect(c)
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)

    # Calcular el tamaño relativo de la placa
    image_width = image.shape[1]
    image_height = image.shape[0]
    plate_width = w
    plate_height = h

    relative_width = plate_width / image_width
    relative_height = plate_height / image_height

    # Ajusta estos umbrales según tus necesidades
    max_relative_width = 0.3
    max_relative_height = 0.15

    if 0.01 < relative_width < max_relative_width and 0.01 < relative_height < max_relative_height or len(approx) == 4:
        cv2.drawContours(image, [c], 0, (0, 225, 0), 2)
        aspect_ratio = float(w) / h
        if aspect_ratio > 2.4:
            placa = gray[y:y + h, x:x + w]
            text = pytesseract.image_to_string(placa, config='--psm 11')
            if len(text) > 6:
                print('len =', len(approx))
                print('area= ', area)
                print('text= ', text)
                cv2.imshow('placa', placa)
                cv2.moveWindow('placa', 780, 10)

cv2.imshow('Image', image)
cv2.imshow('Canny', canny)
cv2.moveWindow('Image', 45, 10)
cv2.waitKey(0)
