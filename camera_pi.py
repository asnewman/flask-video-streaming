import io
import time
import datetime as dt
import os
import sys
import picamera
import json
from base_camera import BaseCamera
from emailer import Emailer
import cv2

class Camera(BaseCamera):
    @staticmethod
    def frames(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (480, 560)
            camera.annotate_text_size = 20 # (values 6 to 160, default is 32)
            camera.annotate_text = dt.datetime.now().strftime('%A %d %b %Y')

            # let camera warm up
            time.sleep(2)

            # Send an email to the user with a screen cap
            if (os.getenv('SEND_EMAIL') == 'true'):
                send_to = os.getenv('RECEPIENT_EMAIL')

                print("Sending image capture to " + send_to)

                sender = Emailer()

                email_subject = "New image taken at " + str(dt.datetime.now())
                image_location = '/home/pi/Desktop/tmp.jpg'
                camera.capture(image_location)

                sender.sendmail(send_to, email_subject, image_location)

            # Start streaming
            stream = io.BytesIO()
            qr_code_check_counter = 0
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                qr_code_check_counter += 1
                if (qr_code_check_counter == 1000) {
                    self.handle_qr_check(camera)
                    qr_code_check_counter = 0
                }

                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

    def qr_decoder(image_location):
        image = cv2.imread(image_location)
        qr_code_detector = cv2.QRCodeDetector()
        # will be none if no QR code is found
        return qr_code_detector.detectAndDecode(image)
    
    def handle_qr_check(camera):
        image_location = '/home/pi/Desktop/tmp.jpg'
        camera.capture(image_location)
        decoded_qr_code = self.qr_decoder(image_location)
        
        if (decoded_qr_code != "") {
            new_data = json.load(decoded_qr_code)
            with open('.env', 'w') as f:
                env_vars = ["SEND_EMAIL", "SENDER_EMAIL", "SENDER_EMAIL_PASSWORD", "RECEPIENT_EMAIL"]
                for var : env_vars:
                    f.write(f'{var}={new_data[var] if new_data[var] != None else os.getenv(var)}\n')
                f.close()

            os.execv(__file__, sys.argv)
        }