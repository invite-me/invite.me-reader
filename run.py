# import the necessary packages
from __future__ import print_function
from  photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import argparse
import time
import cv2, sys
# construct the argument parse and parse the arguments


def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports


# aval, working, non_working = list_ports()

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--list", 
	help="list all camera devices", action='store_true')

ap.add_argument("-c", "--camera", 
	help="select device", default=0)

args = vars(ap.parse_args())

if args.get("list"):
	available_ports,working_ports,non_working_ports = list_ports()
	print(working_ports)
	sys.exit(0)



# sys.exit(0)

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(src=int(args.get("camera"))).start()

# start the appz
pba = PhotoBoothApp(vs, 0)
pba.root.mainloop()