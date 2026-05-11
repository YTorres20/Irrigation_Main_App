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

        self.mode = None

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

        self.set_up_grid(weights=1)
        self.main_button_frame = ctk.CTkFrame(self)
        self.main_button_frame.grid(row=1,column=1)

       ######### Entry point for soil moisture collections #######
        self.soil_button = ctk.CTkButton(
            self.main_button_frame,
            text="Soil Moisture",
            command=self.show_soil_menu
        )
        self.soil_button.grid(padx=10, pady=10)

        self.veg_button = ctk.CTkButton(
            self.main_button_frame,
            text="Vegetable Health",
            command=self.show_veg_menu
        )
        self.veg_button.grid()



        # Apply centralized styling to UI components
        styler.style_button(self.soil_button)
        styler.style_button(self.veg_button)
        styler.style_main_label(self.welcome_label)
        styler.style_window(self)

        
    
    def show_soil_menu(self):
        self.clear_window()
        self.mode = "soil"

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.grid(row=1,column=1)

        self.record_button = ctk.CTkButton(
            self.menu_frame,
            text="Record Data",
            command=self.open_record_windows
        )
        self.record_button.grid(padx=10, pady=10)

        # Entry for AI-training 
        self.YOLO_button = ctk.CTkButton(
            self.menu_frame,
            text="Run YOLO",
            command=self.open_training_windows
        )
        self.YOLO_button.grid()

        styler.style_button(self.record_button)
        styler.style_button(self.YOLO_button)

    def show_veg_menu(self):
        self.clear_window()
        self.mode = "vegetable"

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.grid(row=1,column=1)

        self.record_button = ctk.CTkButton(
            self.menu_frame,
            text="Record Data",
            command=self.open_record_windows
        )
        self.record_button.grid(padx=10, pady=10)

        styler.style_button(self.record_button)


    # Configure grid layout to center content vertically and horizontally
    def set_up_grid(self,rows=3,columns=3, weights=0):
        for r in range(rows):
            self.grid_rowconfigure(r,weight=weights)
        for c in range(columns):
            self.grid_columnconfigure(c,weight=weights)


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
    
    def clear_window(self):
        for widgets in self.winfo_children():
            widgets.destroy()
    
