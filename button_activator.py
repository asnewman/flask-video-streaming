import RPi.GPIO as GPIO
import requests
import signal

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)

def main():
	signal.signal(signal.SIGALRM, handler)
	while True:
		if GPIO.input(16) == 1:
			print('button pressed')
			signal.alarm(5)
			request_camera()
			print('request done')


def request_camera():
	requests.get("http://localhost:5000/video_feed")


def handler(signum, frame):
	main()


if __name__	== '__main__':
	main()