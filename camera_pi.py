import io
import time
import datetime as dt
import os
import picamera
from base_camera import BaseCamera
from emailer import Emailer

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            #camera.resolution = (320, 240)
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
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
