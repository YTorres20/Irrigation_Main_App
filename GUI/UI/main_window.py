# UI components 
import customtkinter as ctk
import GUI.UI.Utils.UI_settings as constant 
import GUI.UI.Utils.styler as styler

# Core application windows 
from GUI.UI.record_windows import RecordingSession
from GUI.UI.training_windows import TrainingSession 

# Core system and path management
from GUI.Collections.Core.system_manager import SystemManager
from GUI.Collections.Core.path_manager import PathManager

# Hardware and backend logic
from GUI.Collections.Device.camera import Camera 
from GUI.Collections.Core.recorder import Recorder
from GUI.Collections.Core.trainer import Trainer


class App(ctk.CTk):
    """
    Main application window for the Irrigation Main App.
    Acts as the central controller that initializes system resources,
    backend managers, and the primary GUI components.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # System-level manager (OS, platform-specific behavior)
        self.system = SystemManager()

        # Centralized file and directory management
        self.file_system = PathManager()

        # Prepares the camera interface using system-specific setting
        self.camera = Camera(self.system)

        # Recorder handles image capture, storage, and data upload
        self.recorder = Recorder(self.file_system)

        # Trainer manages dataset download and YOLO training
        self.trainer = Trainer(self.file_system)

        self.geometry("700x700+5000")
        self.title("IRRIGATION MAIN")

        self.welcome_label = ctk.CTkLabel(self, text=constant.WELCOME_MESSAGE)
        self.welcome_label.grid(row=0, column=1)

        # Entry point for data collections
        self.record_button = ctk.CTkButton(
            self,
            text="Record Data",
            command=self.open_record_windows
        )
        self.record_button.grid(row=1, column=1, padx=20, pady=20)

        # Entry for AI-training 
        self.YOLO_button = ctk.CTkButton(
            self,
            text="Run YOLO",
            command=self.open_training_windows
        )
        self.YOLO_button.grid(row=2, column=1, padx=20, pady=20)

        # Apply centralized styling to UI components
        styler.style_button(self.record_button)
        styler.style_button(self.YOLO_button)
        styler.style_main_label(self.welcome_label)
        styler.style_window(self)

        # Configure grid layout to center content vertically and horizontally
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
    
    def open_record_windows(self):
        """
        Launches the recording session window.
        Handles user input, image capture workflow, and data upload.
        """
        session = RecordingSession(self)
        session.set_recording_file()

    def open_training_windows(self):
        """
        Launches the training session window.
        Handles dataset download and automated YOLO training.
        """
        session = TrainingSession(self)
        session.set_training_session()


