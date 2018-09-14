'''
A class for automaically switching/configuring camera modes.
Calls 'v4l2-ctl' to set the parameters for the camera's on the fly.
'''

import os
import cv2

class config:

	# get the default parameters for the camera
	def __init__(self, cameras):
		os.system("v4l2-ctl -i")
		# this does not do anything. need to investigate if switching on/off the LED strip would work to detect the goals.

	# Sets the camera to HSV settings for goal seeking.
	def setCameraToHSV(cameraID):
		os.system("v4l2-ctl -d /dev/video{} -c brightness=80 -c contrast=0 -c saturation=200 -c white_balance_temperature_auto=0 -c power_line_frequency=2 -c white_balance_temperature=10000 -c sharpness=0 -c exposure_auto=1 -c exposure_absolute=5 -c pan_absolute=0 -c tilt_absolute=0 -c zoom_absolute=0".format(cameraID))


	def setCameraToDefault(cameraID):
		os.system("v4l2-ctl -d /dev/video{} i ")

	# stops the camera being used in cv2
	def unlinkCameraFromCV(cameraID):
		camera = cv2.VideoCapture(cameraID)
		camera.release
