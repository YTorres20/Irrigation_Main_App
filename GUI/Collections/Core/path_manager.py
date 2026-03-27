from pathlib import Path

class PathManager():
    """
    Manage project's directories and file paths for data collection, post-processing,
    and training workflows. It relies on a fixed project root and automatically and automatically 
    creates necessary directories for recordings, training datasets, and results. 
    Paths for YOLO training scripts, fonts, and RoboFlow tokens are also provided. 

    relies on set_recording_name() and set_training_session.
    """
    def __init__(self):
        self._project_root = Path(__file__).resolve().parent.parent.parent.parent
        self._base_data = self._project_root/"GUI/Collections/DataCollection/Data"
        self._base_post = self._project_root/"GUI/Collections/DataCollection/Post-Processing"
        self._base_training = self._project_root/"GUI/Collections/Training/Sessions"

        self._training_path = None  #  will include _base_training and training session name 

        self.yolo_train_file = self._project_root/"GUI/Collections/YOLO/train.py"
        self.font_path = self._project_root/"Assets/Fonts/ttf/DejaVuSans.ttf"
        
        self.token_path = self._project_root/"GUI/Collections/RoboFlow/.env"

        self.recording_name = None 
        self.training_name = None 

        self.data_path = None
        self.post_path = None 
        self.training_data_path = None 
        self.training_result_path = None

    def set_recording_name(self,file_name:str):
        """
        Creates Data and Post-processing directories.
        """
        self.recording_name = file_name 
        self.data_path = Path(self._base_data)/self.recording_name
        self.post_path = Path(self._base_post)/self.recording_name

        self.data_path.mkdir(parents=True, exist_ok=True)
        self.post_path.mkdir(parents=True, exist_ok=True)

    def set_training_name(self,file_name:str):
        """
        Creates Datasets and Result directories
        """
        self.training_name = file_name
        self._training_path = Path(self._base_training)/self.training_name
        self._training_path.mkdir(parents=True, exist_ok=True)

        self.training_result_path = self._training_path/"Result"
        self.training_result_path.mkdir(parents=True,exist_ok=True)

        self.training_data_path = self._training_path/"Datasets"
        self.training_data_path.mkdir(parents=True, exist_ok=True)
