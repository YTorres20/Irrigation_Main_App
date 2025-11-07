from   GUI.DataCollection.Recording.camera import Camera
import GUI.DataCollection.Recording.consolidate as consolidate
import GUI.DataCollection.RoboFlow.roboflow as Robo
from pathlib import Path
import time
import os
import platform
import cv2

MOISTURE_DATA = []

WELCOME_MESSAGE = "Welcome!"
FILE_QUESTION = "Please enter the name of this recording's file: "
ERROR_INPUT = "Invalid input! No special characters ($,@,!,..)! No spaces!"
ERROR_INPUT_TWO = "Invalid input!"
DATA_PROMPT = "Enter the moisture (format: x.x, example: 1.3) or q to quit: "
CONSOLIDATION_LABEL = "Consolidating..."
CONSOLIDATION_ERROR_LABEL = "Data was not consolidated!"
ROBOFLOW_UPLOAD_LABEL = "Data has been uploaded to RoboFlow"

VIDEO_WIDTH_LENGTH = (1280,720) # HD resolution
CAMERA_SETTING = None
CAMERA_BACKEND = None

FOLDER_NAME = None
OPEN_PATH = None
STORAGE_PATH = "GUI/DataCollection/Data"
POST_PROCESSING_PATH = "GUI/DataCollection/Post-Processing"
PATH_TO_TOKENS = "GUI/DataCollection/RoboFlow/.env"

def get_camera_device():
    system = platform.system()
    
    if system == "Linux":
        devices = [f"/dev/{d}" for d in os.listdir("/dev") if d.startswith("video")]
        if not devices:
            print("❌ No camera device found under /dev/")
            return 0, cv2.CAP_V4L2
        return devices[0], cv2.CAP_V4L2
    
    elif system == "Windows":
        return 0, cv2.CAP_DSHOW
    
    elif system == "Darwin":
        return 0, cv2.CAP_AVFOUNDATION
    
    else:
        return 0, cv2.CAP_ANY


def validate_input(user_input:str) -> bool: 
  user_input = user_input.strip()

  if not user_input:
      return False 
  if all(ch.isalnum() or ch == "_" or ch == "-" for ch in user_input):
      return True
  else: 
      return False
           
def TurnCameraOn() -> Camera:
    global CAMERA_SETTING , CAMERA_BACKEND
    CAMERA_SETTING, CAMERA_BACKEND = get_camera_device()
    return Camera()
    
def GetFrame(Camera_obj:Camera):
    Camera_obj.UpdateFrames()
    return Camera_obj.img

def Snap(Camera_obj:Camera):
    file_name = OPEN_PATH / f"photo_{int(time.time())}.png"
    Camera_obj.img.save(file_name)
    print(f"✅ Photo saved: {file_name}")

def SetFolderName(folder_name:str) -> None:
    global FOLDER_NAME
    FOLDER_NAME= folder_name

    global OPEN_PATH
    OPEN_PATH = Path(STORAGE_PATH)/FOLDER_NAME 
    OPEN_PATH.mkdir(parents=True,exist_ok=True)

def TurnOffCamera(Camera_obj:Camera):
    Camera_obj.Release()

def UpdateMoistureData(data):
    global MOISTURE_DATA
    MOISTURE_DATA.append(data)

def CreateCSV():
    csv_path = OPEN_PATH / "moistures.csv"
    with open(csv_path, "w") as f:
        f.write("Moisture\n")
        for mo in MOISTURE_DATA:
            f.write(f"{mo}\n")

def ConsolidateData():
    output_path = Path(POST_PROCESSING_PATH)/FOLDER_NAME
    completed = consolidate.ConsolidateData(image_folder=OPEN_PATH,output_folder=output_path)
    return completed

def upload_data():
    post_images = Path (POST_PROCESSING_PATH)/FOLDER_NAME
    post_images = str(post_images)
    Robo.upload_data(post_images,FOLDER_NAME)