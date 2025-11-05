# Irrigation Main App - Ubuntu Setup 

## Overview
The **Irrigation Main App** is a graphical user interface (GUI) built with **Python** and **CustomTkinter** to assist with soil moisture data collection and image post-processing.  

It provides tools for recording images using a camera module, consolidating those images with corresponding soil moisture readings, and preparing them for upload (e.g., to Roboflow for AI training).

---
## Features 

### User-Friendly GUI
- Built using **CustomTkinter** for a modern interface.  
- Provides intuitive dialogs and visual feedback.  
- Modular layout allows easy extension for new tools (e.g., Roboflow upload, data visualization, etc.).  

### Camera Recording
- Captures and stores images directly from the connected camera.  
- Automatically saves each captured image in the `GUI/DataCollection/Data` directory.  

###  Data Consolidation
- Combines recorded images with corresponding moisture readings stored in a CSV file (`moistures.csv`).  
- Draws the moisture value directly on each image.  
- Saves consolidated images into the `Post-Processing` folder.  
- Prevents continuation if `moistures.csv` is empty or missing valid data.  

---

##  Project Structure
```
Irrigation-Main-App/
│
├── application.py
├── GUI/
│   ├── MainWindow.py
│   ├── helper.py
│   ├── styler.py
│   ├── RecordWindow.py
│   │
│   └── DataCollection/
│       ├── Data/               # Captured images
│       ├── Post-Processing/    # Consolidated images + CSV
│       ├── Recordings/
│       │   ├── camera.py
│       │   └── consolidate.py
│       ├── RoboFlow/
│       │   ├── roboflow.py     # Roboflow upload logic
│       │   └── .env            # API key, workspace, project ID           
│       └── YOLO/               
│      
└── README.md
```
---

## Setup

---

### Force Python 3.11
Ubuntu 23+ defaults to Python 3.12, which breaks numpy and some packages.
Change your instructions to explicitly use Python 3.11.

`Conda method (recommended):`
```bash
conda create -n app python=3.11
```
```bash
conda activate app
```

`venv method:`
```bash
sudo apt install python3.11 python3.11-venv
```
```bash 
python3.11 -m venv app
```
```bash
source app/bin/activate
```
- `Always activate the environment before installing packages or running the app.`

---

### Install System Dependencies (Ubuntu Only)

Ubuntu requires some system packages for Python GUI and OpenCV:
```bash 
sudo apt update
sudo apt install python3-pip python3-tk ffmpeg libgl1 libsm6 libxext6 libxrender-dev -y
```
- python3-tk is required for CustomTkinter.
- ffmpeg and lib* packages are needed for OpenCV video/camera support.

Upgrade pip, setuptools, and wheel:
```bash 
pip install --upgrade pip setuptools wheel packaging numpy

```

---

### Install Python Dependencies

`Navigate to the project folder`

Install dependencies inside the activated environment using the Ubuntu-specific requirements file:
```bash 
pip install -r requirements-ubuntu.txt
```

---

### Run the Application
```bash 
python application.py
```

---

### Workflow
- Launch the GUI.
- Record data via the camera.
- Consolidate moisture readings and images.
- Upload to Roboflow if needed.

## Future Enhancements
- **Roboflow integration:** Downloading datasets directly from the GUI
- AI-based soil moisture prediction  

## Notes for Developers
- The **camera** module uses OpenCV for image capture.  
- The **consolidation** module checks for a valid CSV and prevents proceeding if the file is empty.  
- The **helper.py** module:
  - Connects messages and feedback to the GUI.
  - Serves as the bridge between backend logic and the user interface.
---
### Author:
Developed by **Yarely Torres** <br>
Project: Irrigation Main App – AI-Powered Soil Moisture Monitoring
