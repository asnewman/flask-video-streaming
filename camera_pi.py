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
    @classmethod
    def frames(cls):
        with picamera.PiCamera() as camera:
            camera.resolution = (480, 560)
            # camera.resolution = (1920, 1080)
            camera.annotate_text_size = 20 # (values 6 to 160, default is 32)
            camera.annotate_text = dt.datetime.now().strftime('%A %d %b %Y')

            # let camera warm up
            time.sleep(2)

            # Send an email to the user with a screen cap
            print(f"Configured email: {os.getenv('SENDER_EMAIL')}")
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
                if (qr_code_check_counter == 100):
                    cls.handle_qr_check(camera)
                    qr_code_check_counter = 0

                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

    @classmethod
    def qr_decoder(cls, image_location):
        image = cv2.imread(image_location)
        qr_code_detector = cv2.QRCodeDetector()
        # will be none if no QR code is found
        return qr_code_detector.detectAndDecode(image)
   
    @classmethod
    def handle_qr_check(cls, camera):
        image_location = '/home/pi/Desktop/tmp.jpg'
        camera.capture(image_location)
        decoded_qr_code, points, _ = cls.qr_decoder(image_location)
        
        if (decoded_qr_code == ""):
            print("No qr code found")
        else:
            print(decoded_qr_code)
            new_data = json.loads(decoded_qr_code)
            env_vars = ["SEND_EMAIL", "SENDER_EMAIL", "SENDER_EMAIL_PASSWORD", "RECEPIENT_EMAIL"]
            if len([key for key in new_data if key in env_vars]) > 0:
                print("updating env variables")
                with open('.env', 'w') as f:
                    for var in new_data.keys():
                        f.write(f'{var}={new_data[var] if new_data[var] != None else os.getenv(var)}\n')
                    f.close()

                camera.close()
                os.execv(sys.executable, ['python'] + [os.path.abspath(sys.argv[0])])
