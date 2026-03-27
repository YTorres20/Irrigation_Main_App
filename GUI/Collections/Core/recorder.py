
from GUI.Collections.RoboFlow.roboflow import RoboFlow

from GUI.Collections.DataCollection.Processing.consolidate import consolidate_data

class Recorder():
    """
    Manages the data collection workflow, collects and stores the numeric data entries,
    handles the creation of the csv file, provides a bridge for the consolidation process, and 
    handles the upload of consolidated data onto Roboflow. 

    This class is initialized with a reference of the PathManager class.
    """
    def __init__(self,paths):
      self._paths = paths 
      self._csv_name = "moistures.csv"
      self._moisture_data = []

    def record(self,data:float):
        """
        Records a single numeric entry into memory
        """
        self._moisture_data.append(data)

    def create_csv(self):
       self._data_path = self._paths.data_path/self._csv_name
       with open(self._data_path,"w") as f:
           f.write("Moisture\n")
           for mo in self._moisture_data:
               f.write(f"{mo}\n")

    def consolidation(self) -> bool:
        """
        Processes images along with numeric entries into Post-processing.
        Returns true on success 
        """
        return consolidate_data(self._paths.data_path,self._paths.post_path)

    def upload_data(self):
        robo = RoboFlow(self._paths.token_path)
        robo.upload_data(self._paths.post_path,self._paths.recording_name)
        print("\nUpload complete\n")
        
        
       
       
      



   
      



    

