import roboflow 
import os
from dotenv import load_dotenv


def upload_data(path:str,batch_name:str)->None:
    
    load_dotenv()
    key= os.getenv("ROBOFLOW_KEY")
    ID = os.getenv("PROJECT_ID")
    workspace = os.getenv("WORKSPACE")
    
    if not key or not ID or not workspace:
        raise ValueError("Make sure ROBOFLOW_KEY, WORKSPACE, and PROJECT_ID are set in .env")

    rf = roboflow.Roboflow(api_key=key)
    workspace = rf.workspace(workspace)

    workspace.upload_dataset(
        path,
        ID, 
        project_license="MIT", 
        project_type= "object-detection", 
        num_workers=10,
        num_retries=3, 
        batch_name=batch_name,
        is_prediction=True
          )



