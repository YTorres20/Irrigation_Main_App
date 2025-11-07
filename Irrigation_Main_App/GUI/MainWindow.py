import customtkinter as ctk
from . import styler
from . import RecordWindows
from . import helper

class app(ctk.CTk):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.geometry("700x700+5000")
        self.title("IRRIGATION MAIN")

        self.record_button = ctk.CTkButton(self, text= "Record Data", command=lambda:RecordWindows.SetRecordingFile(parent=self) )
        self.record_button.grid(row=1, column=1, padx=20, pady=20)
        styler.StyleButton(self.record_button)

        self.welcome_label = ctk.CTkLabel(self, text=helper.WELCOME_MESSAGE)
        self.welcome_label.grid (row=0, column=1)

        styler.StyleMainLabel(self.welcome_label)
        styler.StyleWindow(self)


        for i in range (3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight = 1)

