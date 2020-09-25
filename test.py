import cv2
from pyzbar import pyzbar

cap = cv2.VideoCapture(0)


while True:
    _, img = cap.read()
    barcodes = pyzbar.decode(img)
    
    for barcode in barcodes:
        data = barcode.data.decode('ascii')
        cap.release()
        print(data)
        break
            