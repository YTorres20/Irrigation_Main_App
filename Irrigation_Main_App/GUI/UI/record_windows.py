
import customtkinter as ctk 

# UI components 
import GUI.UI.Utils.styler as styler
import GUI.UI.Utils.UI_settings as constant

from GUI.UI.Utils.validation import validate_input

class RecordingSession:
    """
    Manages the data collection workflow for appilcation.
    It prompts the user to enter a recording name, collects numeric 
    data entries while capturing images from the camera, consoildates 
    the data into csv file, and uploads the dataset to RoboFlow for training 

    This class is initialized with a reference to main appilication and is started 
    by calling the set_recording_file() method. 

    """
    def __init__(self,app):
        self.app = app

        self.dialog = None
        self.data_window = None 
        self.camera_window = None 

    #--------------Recording Name______________#

    def set_recording_file(self):
        self.dialog = ctk.CTkToplevel(self.app)
        self.dialog.geometry("550x100+600+400")
        self.dialog.title("USER INPUT")
        self.dialog.transient(self.app)
        self.dialog.update()
        self.dialog.grab_set() # modal

        self.dialog.label = ctk.CTkLabel(self.dialog,text=constant.FILE_QUESTION)
        self.dialog.label.grid(row=0,column=0)
        self.dialog.entry = ctk.CTkEntry(self.dialog,placeholder_text="e.g: Recording_one")
        self.dialog.entry.grid(row=0, column=1,padx=10,pady=10)
       

        styler.style_window(self.dialog)
        styler.style_label(self.dialog.label)

        self.dialog.entry.bind("<Return>",lambda event: self._submit())

    def _submit(self) -> None:
        user_input = self.dialog.entry.get()
        self.dialog.input_error_label = ctk.CTkLabel(self.dialog,text=constant.ERROR_INPUT)
        styler.style_error_label(self.dialog.input_error_label)

        if (validate_input(user_input)):
            self.dialog.destroy()
            self.app.file_system.set_recording_name(user_input)
            self._start_recording()
        else:
            self.dialog.input_error_label.grid(row=1, column=0)
            self.dialog.entry.delete(0, ctk.END) 
    
    #---------------Recording-----------------#

    def _start_recording(self) -> None:
        """
        Opens the data entry and camera windows and begins capturing images. 
        Does not return until recording is complete.
        """
        self.data_window = ctk.CTkToplevel(self.app)
        self.data_window.geometry("600x200+750+350")
        self.data_window.title("DATA")
        self.data_window.transient(self.app)
        self.data_window.update()  
        self.data_window.grab_set() # modal 
    
        self.data_window.label = ctk.CTkLabel(self.data_window, text=constant.DATA_PROMPT)
        self.data_window.label.grid(row=0, column=0)
        self.data_window.entry = ctk.CTkEntry(self.data_window)
        self.data_window.entry.grid(row=0, column=1, padx=10, pady=10)
        self.data_window.entry.focus_set() 

        styler.style_label(self.data_window.label)
        styler.style_window(self.data_window)

        self.camera_window = ctk.CTkToplevel(self.app)
        self.camera_window.geometry("700x700")
        self.camera_window.title("CAMERA")
        self.camera_window.transient(self.app)
        self.camera_window.update()  

        styler.style_window(self.camera_window)

        self.camera_window.image_label = ctk.CTkLabel(self.camera_window, text=None)
        self.camera_window.image_label.grid(row=0, column=0)

        self.app.camera.set_storage(self.app.file_system.data_path)
        self.app.camera.on()
        self._display_camera()

        self.data_window.entry.bind("<Return>", lambda event:self._gather_data())

    #----------------Camera----------------#

    def _display_camera(self):
        frame = self.app.camera.update_frame()
        video = ctk.CTkImage(light_image=frame, size=self.app.camera.VIDEO_WIDTH_LENGTH)
        self.camera_window.image_label.configure(image=video)
        self.after_id = self.camera_window.after(10, lambda: self._display_camera())

    #--------------Data-------------------#

    def _gather_data(self):
        """
        Reads user input, validates it, captures a photo, and records the data. 
        Quits reading if the user enters 'q'
        """
        data = self.data_window.entry.get()
        if data.strip() == "q":
            self.data_window.destroy()
            self.camera_window.destroy()
            self.app.camera.stop()
            self.camera_window.after_cancel(self.after_id)
            self.after_id = None
            self.data_window = None
            self.camera_window = None
            self.app.recorder.create_csv()
            self._consolidate()
            return
        if hasattr(self.data_window, "input_error_label") and self.data_window.input_error_label:
            self.data_window.input_error_label.destroy()
            self.data_window.input_error_label = None
        try:
            data = float(data)
        except ValueError:
            self.data_window.input_error_label = ctk.CTkLabel(self.data_window, text=constant.ERROR_INPUT_TWO)
            self.data_window.input_error_label.grid(row=1, column=0)
            styler.style_error_label(self.data_window.input_error_label)
            self.data_window.entry.delete(0, ctk.END)
            return 
    
        self.app.camera.take_photo()
        self.app.recorder.record(data)
        self.data_window.entry.focus_set()
        self.data_window.entry.delete(0, ctk.END)

    #-----------------consolidation----------------#

    def _consolidate(self):
        """
        Consolidates recorded data into CSV and triggers RoboFlow upload. 
        """
        self.dialog = ctk.CTkToplevel(self.app)
        self.dialog.geometry("550x100+600+400")
        self.dialog.title("CONSOLIDATION")
        self.dialog.transient(self.app)
        self.dialog.update() 
        self.dialog.grab_set()

        styler.style_window(self.dialog)

        self.dialog.spinner_label = ctk.CTkLabel(self.dialog, text="|", font=("Arial", 24))
        self.dialog.spinner_label.grid(row=0, column=1, padx=20, pady=20)

        consolidating_label = ctk.CTkLabel(self.dialog, text=constant.CONSOLIDATION_LABEL)
        consolidating_label.grid(row=1, column=1)

        styler.style_label(consolidating_label)

        for i in range(3):
            self.dialog.grid_rowconfigure(i, weight=1)
            self.dialog.grid_columnconfigure(i, weight=1)

        # spinner
        symbols = ["|", "/", "-", "\\"]
        def spin(i=0):
            self.dialog.spinner_label.configure(text=symbols[i % len(symbols)])
            self.after_id=self.dialog.spinner_label.after(100, lambda: spin(i + 1))
        spin()

        if self.app.recorder.consolidation():
            self.dialog.destroy()
            self.dialog.after_cancel(self.after_id)
            self.after_id = None 
            self._roboflow()
        else:
            self.dialog.error_label = ctk.CTkLabel(self.dialog, text=constant.CONSOLIDATION_ERROR_LABEL)
            self.dialog.error_label.grid(row=2, column=1)
            styler.style_error_label(self.dialog.error_label)

    #--------------RoboFlow--------------#

    def _roboflow(self):
       """
       Uploads consolidated data to RoboFlow and bring terminal to the front. 
       """
       self.app.system.bring_terminal_to_front()
       self.app.recorder.upload_data()
       print("If done, please exit.")


    
