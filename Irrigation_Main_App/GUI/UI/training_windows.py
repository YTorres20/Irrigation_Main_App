
import customtkinter as ctk 

# UI components
import GUI.UI.Utils.styler as styler 
import GUI.UI.Utils.UI_settings as constant 

from GUI.UI.Utils.validation import validate_input

class TrainingSession:
    """
    Manages training workflow for the application.
    It prompts user for a training session name and triggers
    the AI-training process. 

    This class is initialized with a reference to the main application and is started 
    by the set_training_session() method.
    """
    def __init__ (self,app):
        self.app = app
        self.dialog = None 

    def set_training_session(self):
        self.dialog = ctk.CTkToplevel(self.app)
        self.dialog.geometry("550x100+600+400")
        self.dialog.title("USER INPUT")
        self.dialog.transient(self.app)
        self.dialog.update()
        self.dialog.grab_set()

        self.dialog.recording_label = ctk.CTkLabel(self.dialog, text=constant.TRAINING_SESSION_PROMP)
        self.dialog.recording_label.grid(row=0, column=0)
        self.dialog.entry = ctk.CTkEntry(self.dialog, placeholder_text="e.g: Training_one")
        self.dialog.entry.grid(row=0, column=1, padx=10, pady=10)

        styler.style_window(self.dialog)
        styler.style_label(self.dialog.recording_label)
    
        self.dialog.entry.bind("<Return>", lambda event: self._submit())
        return

    def _submit(self):
        user_input = self.dialog.entry.get()
        if validate_input(user_input):
            self.dialog.destroy()
            self.app.file_system.set_training_name(user_input)
            self.app.system.bring_terminal_to_front()
            self.app.trainer.begin_training()
        else:
            self.dialog.input_error_label = ctk.CTkLabel(self.dialog, text=constant.ERROR_INPUT)
            self.dialog.input_error_label.grid(row=1, column=0)
            styler.style_error_label(self.dialog.input_error_label)
            self.dialog.entry.delete(0, ctk.END) 
            return




