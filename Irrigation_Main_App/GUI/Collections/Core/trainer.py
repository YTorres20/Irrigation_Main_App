from GUI.Collections.RoboFlow.roboflow import RoboFlow
import yaml
import subprocess
import sys



class Trainer:
    """
    Manages the training and AI-training processes.
    Downloads the versions of dataset from RoboFlow, rewrites the YAML
    file, and triggers YOLO. 

    This class is initialized with a reference of the PathManager class 
    """
    def __init__(self,paths):
        self._paths = paths

    def begin_training(self):
        self._robo = RoboFlow(self._paths.token_path)
        self._dataset_path = self._robo.download_dataset(self._paths.training_data_path)

        self._yaml_file = self._find_yaml_file()
        self._yaml_file = self._yaml_file.resolve()

        self._normalize()
        self._train()

    def _find_yaml_file(self):
        print(f"\nSearching for YAML in:{self._dataset_path}\n")

        self._yaml_file = list(self._dataset_path.rglob("*.yaml"))

        if not self._yaml_file:
            raise FileNotFoundError("Cannot find .yaml file!")
        
        return self._yaml_file[0]

    def _normalize(self):
        """
        Updates the train, val, and test paths in the YAML file to match the downloaded dataset.
        """

        with open (self._yaml_file,"r") as file:
            content = yaml.safe_load(file)
        
        content["train"] = str(self._dataset_path/"train/images")
        content["val"] = str(self._dataset_path/"valid/images")
        content["test"] = str(self._dataset_path/"test/images")

        with open (self._yaml_file,"w") as file:
            yaml.safe_dump(content,file)

    def _train(self):
        command = [
            sys.executable,
            str(self._paths.yolo_train_file),
            "--img", "640",
            "--batch","15",
            "--epochs","100",
            "--data",str(self._yaml_file),
            "--weights","yolov5s.pt",
            "--project", str(self._paths.training_result_path),
        ]
        subprocess.run(command,check=True)
        print("\nTraining complete. Results are in the Training folder.\n")








        