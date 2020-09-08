from imutils.ivdeo import VideoStream
from pyzbar import pyzbar

class QRScanner:
    @staticmethod
    def startScanning():

        cap = VideoStream(usePiCamera=True).start()
        #allow camera to warm up
        time.sleep(2)

        print("Waiting for a QR Code...")
        
        while True:
                
            frame = vs.read()
            codes = pyzbar.decode(frame)
            
            for code in codes:
                data = code.data.decode('ascii')
                cap.stop()
                return data
                
                 
