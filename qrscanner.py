import cv2
from pyzbar import pyzbar

class QRScanner:
    @staticmethod
    def startScanning():

        cap = cv2.VideoCapture(0)

        print("Waiting for a QR Code...")
        
        while True:
                
            _, img = cap.read()
            codes = pyzbar.decode(img)
            
            for code in codes:
                data = code.data.decode('ascii')
                cap.release()
                return data
                
                 
