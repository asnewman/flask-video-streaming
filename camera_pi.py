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
import numpy as np
import RPi.GPIO as GPIO
from autofocus import run_autofocus


RELAY_PIN = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(RELAY_PIN, GPIO.OUT)

class Camera(BaseCamera):
    @classmethod
    def frames(cls):
        with picamera.PiCamera() as camera:
            camera.resolution = (480, 560)
            # camera.resolution = (720, 840)
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
            qr_code_check_counter = 99

            do_autofocus = False
            autofocus_counter=999
            max_index = 10
            max_value = 0.0
            last_value = 0.0
            dec_count = 0
            focal_distance = 10

            for frame in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                

                # return current frame
                stream.seek(0)
                curr_frame = stream.read()
                yield curr_frame

                autofocus_counter += 1
                if autofocus_counter == 1000:
                    do_autofocus = True
                    max_index = 10
                    max_value = 0.0
                    last_value = 0.0
                    dec_count = 0
                    focal_distance = 10
                    autofocus_counter = 0

                if do_autofocus:
                    autofocus_result = run_autofocus(curr_frame, max_index, max_value, last_value, dec_count, focal_distance)
                    print(autofocus_result)

                    if not autofocus_result:
                        print('continuing autofocus')
                        max_index = autofocus_result["max_index"]
                        max_value = autofocus_result["max_value"]
                        last_value = autofocus_result["last_value"]
                        dec_count = autofocus_result["dec_count"]
                        focal_distance = autofocus_result["focal_distance"]
                    else:
                        print('Done autofocusing')
                        do_autofocus = False
                
                qr_code_check_counter += 1
                if (qr_code_check_counter == 100):
                    qr_code_detector = cv2.QRCodeDetector()
                    bytes = np.asarray(bytearray(curr_frame), dtype=np.uint8)
                    cv_image = cv2.imdecode(bytes, cv2.IMREAD_COLOR)
                    decoded_qr_code, points, _ = qr_code_detector.detectAndDecode(cv_image)
                    if (decoded_qr_code != ""):
                        print(decoded_qr_code)
                        new_data = json.loads(decoded_qr_code)
                        print(new_data)
                        if ("DEVICE_PASSWORD" in new_data):
                            correct_code = os.getenv('DEVICE_NUMBER') + os.getenv('DEVICE_PASSWORD')
                            given_code = new_data['DEVICE_CODE'] + new_data['DEVICE_PASSWORD']
                            print(given_code, correct_code)
                            if (correct_code == given_code):
                                print('code accepted')
                                GPIO.output(RELAY_PIN, GPIO.HIGH)
                                time.sleep(3)
                                GPIO.output(RELAY_PIN, GPIO.LOW)


                        env_vars = ["SEND_EMAIL", "SENDER_EMAIL", "SENDER_EMAIL_PASSWORD", "RECEPIENT_EMAIL"]
                        if len([key for key in new_data if key in env_vars]) > 0:
                            print("updating env variables")
                            with open('.env', 'w') as f:
                                for var in new_data.keys():
                                    f.write(f'{var}={new_data[var] if new_data[var] != None else os.getenv(var)}\n')
                                f.close()
            
                            camera.close()
                            os.execv(sys.executable, ['python'] + [os.path.abspath(sys.argv[0])])

                    qr_code_check_counter = 0
                
                qr_code_check_counter += 1
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
