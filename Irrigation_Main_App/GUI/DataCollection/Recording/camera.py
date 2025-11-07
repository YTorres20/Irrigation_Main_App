
import cv2
from PIL import Image
import GUI.helper as helper 

class Camera ():
	def __init__(self):	
		#Webcam
		self.cam  = cv2.VideoCapture(helper.CAMERA_SETTING, helper.CAMERA_BACKEND)
		self.img = None

		if not self.cam.isOpened():
			print("ERROR: could not open video source!")
			exit()

	def UpdateFrames(self):
		ret, frame = self.cam.read()
		if ret:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			frame = cv2.flip(frame,1)
			self.img = Image.fromarray(frame)
				
	def Release(self):
		self.cam.release()


			

		
        




