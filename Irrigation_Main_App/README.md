# Irrigation Main App

## Overview
The **Irrigation Main App** is a graphical user interface (GUI) built with **Python** and **CustomTkinter** to assist with soil moisture data collection, image post-processing, and automated AI training.

It provides an end-to-end workflow for recording images using a camera module, consolidating those images with corresponding soil moisture readings, and automatically triggering `YOLO training` using Roboflow-managed datasets.


## Features

## User-Friendly GUI 
- Built using CustomTkinter for a modern interface
- Provides intuitive dialogs and visual feedback
- Modular layout allows easy extension for new tools (Roboflow, training, visualization)

<img src="Assets/Images/MainWindow.png" alt="Main Window" width="500" height="500">

## Camera Recording
- Captures and stores images directly from the connected camera
- Automatically saves each captured image in the data collection directory 

<img src="Assets/Images/DataCollection.png" alt="Data Collection" width="600" height="500">
<img src="Assets/Images/UserInput.png" alt="User Input" width="500" height="500">

##  Data Consolidation
- Combines recorded images with corresponding moisture readings stored in `moistures.csv`
- Draws the moisture value directly onto each image
- Saves consolidated images into the `Post-Processing` directory
- Prevents continuation if `moistures.csv` is missing or empty 

<img src="Assets/Images/Consolidation.png" alt="Consolidation" width="500" height="500"> 
<img src="Assets/Images/Consolidation_Error.png" alt="Consolidation Error" width="500" height="500">

## Automated YOLO Training
- Fully automated YOLO training pipeline integrated into the application
- Consolidated images are prepared and validated automatically
- Datasets are synced using Roboflow
- YOLO training is triggered programmatically (no manual CLI commands)
- Training runs and outputs are stored in `GUI/Collections/Training/Sessions`

This enables a complete `data collection` → `Roboflow upload `→ `processing` → `training workflow` from a single GUI.

---

##  Project Structure
```
Irrigation-Main-App/
│
├── application.py
├── GUI/
|      ├── Collections/
│      |              ├── Core/
|      |              |       ├── path_manager.py
|      |              |       ├── recorder.py
|      |              |       ├── system_manager.py
|      |              |       ├── trainer.py
|      |              |
|      |              ├── DataCollection/
|      |              |                 ├── Data/
|      |              |                 ├── Post-Processing/
|      |              |                 ├── Processing/
|      |              |                 |             ├── consolidate.py
|      |              ├── Device/
|      |              |         ├── camera.py
|      |              |
|      |              ├── RoboFlow/  
|      |              |           ├── .env
|      |              |           ├── roboflow.py              
|      |              |
|      |              ├── Training/
|      |              |           ├── Sessions/
│      │              |
|      |              ├──YOLO/
|      |
│      └─ UI/
│           ├── main_window.py
│           ├── record_windows.py
|           ├── training_windows.py
|           ├── Utils/
|                    ├── styler.py
|                    ├── UI_settings.py
|                    ├── validation.py
│                  
|
│      
└── README.md
```

---
## Environment Variables
- Roboflow is used for dataset management and automated YOLO training.
- Create a `.env` file in:
```
GUI/Collections/RoboFlow/.env
```
Example:
```
ROBOFLOW_API_KEY=your_api_key_here
WORKSPACE=your_workspace
PROJECT_ID=your_project_id
```
These variables are required only for dataset upload and training-related features.
---
## Recommended Python Version
- Python 3.11 is required for all platforms (macOS, Windows) to ensure full compatibility with dependencies like Pillow, CustomTkinter, and OpenCV.
- Using Python 3.12 or higher may cause build or runtime errors.

`Note: Users do not need to globally replace their system Python. The virtual environment handles the Python version.`
---

## Installing Python 3.11
Installing Python 3.11

`macOS:`
- Download the Python 3.11 macOS installer from [Python.org](https://www.python.org).
- Run the installer — choose Standard Install.
- Verify:
```bash 
python3.11 --version
```
`Windows:`
- Download Python 3.11 from: [Python.org](https://www.python.org).
- During installation:
    - Check “Add Python to PATH”
    - Ensure “Install launcher for all users (recommended)” is enabled
- `The Python Launcher (py) is installed with the official Python installer and is recommended for Windows users. It allows explicit selection of Python versions and prevents version conflicts.`
- Verify:
```bash
python --version
```
- If Python 3.11 does not appear:
```bash
py -3.11 --version
```
---
## Create and Activate a Virtual Environment
` In terminal navigate to the project folder`

- on macOS:
```bash
python3.11 -m venv app
```

- On Windows:
- Option 1 – Standard Method:
```bash
python -m venv app
```
- Option 2 – Recommended (If Multiple Python Versions Are Installed):
```bash
py -3.11 -m venv app
```
`The Python Launcher (py) is recommended on Windows because it allows you to explicitly select Python 3.11 and prevents version conflicts if multiple Python versions are installed.`

#### Activate Virtual Environment:
- On macOS
```bash
source app/bin/activate     
```
- On Windows
```bash
.\app\Scripts\Activate
```

---

## Install Required Dependencies:
```bash
pip install --upgrade pip setuptools wheel
```
```bash
pip install -r requirements.txt
```
```bash
pip install -r yolo-requirements.txt
```
### Running the Application:
```bash
python application.py
```
---
## Windows Training Error: WinError 1114
- If the app crashes with a DLL initialization error when starting YOLO, follow these steps to repair your system files:

- Copy and paste this link into your web browser:
```
https://aka.ms/vs/17/release/vc_redist.x64.exe
```
- Run the Installer: Open the downloaded file and click "Install" or "Repair".
- RESTART Your Computer: This step is mandatory for Windows to register the fixed system files.

## Workflow
- Launch the GUI
- Record images using the camera module
- Provide moisture readings via `moistures.csv`
- Run consolidation to embed moisture values into images
- Automatically upload the prepared dataset to Roboflow
- Automatically trigger YOLO training
- Review training sessions and outputs
---
## Error Handling & Safeguards
- Consolidation blocked if `moistures.csv` is missing or empty
- GUI-based error dialogs prevent crashes
- Camera resources are safely released on window close
- Centralized path management avoids filesystem errors
- YOLO training will not start unless valid data exists
---
## Development Notes
- UI logic is isolated under `GUI/UI`
- Core logic and automation reside under `GUI/Collections`
- File paths are centrally managed via `path_manager.py`
- UI components do not directly access hardware or the filesystem
- YOLO training is invoked programmatically, not via CLI
---
## Known Limitations
- Currently supports a single camera device
- Moisture values are provided externally via CSV
- YOLO inference is not yet integrated into the live camera feed
---
### License
- This project is intended for academic and research use.
---
### Author:
Developed by **Yarely Torres** <br>
Project: Irrigation Main App – AI-Powered Soil Moisture Monitoring