import roboflow 
import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path 

class RoboFlow():
    """
    Handles authentication, dataset uploads, and dataset version
    generation/downloads from Roboflow for YOLO training.
    """
    def __init__(self,token_path:str):
        """
        Loads Roboflow credentials from a .env file and validates them.
        """
        load_dotenv(token_path)

        self.key = os.getenv("ROBOFLOW_KEY")
        self.ID = os.getenv("PROJECT_ID")
        self.workspace = os.getenv("WORKSPACE")
        self.downloaded_data_name = None 

        if not self.key or not self.ID or not self.workspace:
            raise ValueError("Make sure ROBOFLOW_KEY, WORKSPACE, and PROJECT_ID are set in .env")
        
    def upload_data(self,path:str,batch_name:str)->None:

        rf = roboflow.Roboflow(api_key=self.key)
        workspace = rf.workspace(self.workspace)

        workspace.upload_dataset(
            str(path),
            self.ID, 
            project_license="MIT", 
            project_type= "object-detection", 
            num_workers=10,
            num_retries=3, 
            batch_name=batch_name,
            is_prediction=True
            )

    def download_dataset(self, path_for_dataset: str):
        """
        Generates a new dataset version with predefined preprocessing,
        augmentation, and split ratios, then downloads it in YOLOv5 format.
        """
        rf = roboflow.Roboflow(api_key=self.key)
        project = rf.workspace(self.workspace).project(self.ID)

        print("Generating dataset version...")
        date = datetime.now().strftime("%Y-%m-%d") 
        name = f"Version-{date}"

        version = project.generate_version(
         settings={
            "preprocessing": [
                {"name": "resize", "width": 640, "height": 640}
            ],
            "augmentation": [
                {"name": "brightness", "min": -0.2, "max": 0.2},
                {"name": "hue-saturation-value", "hue": 0.1, "saturation": 0.1, "value": 0.1},
                {"name": "noise", "type": "gaussian"},
                {"name": "motion-blur", "radius": 3}
            ],
            "train_split": 0.7,
            "valid_split": 0.2,
            "test_split": 0.1
        }
    )

        print("Created version:", version)

        version = project.version(version)

        dataset = version.download(
            model_format="yolov5",
            location=str(path_for_dataset),
            overwrite=True
        )

        print("Download Complete.")
        print("Dataset location:", dataset.location)

        return Path(dataset.location).resolve()



