import customtkinter as ctk 
from . import styler
from . import helper

def SetRecordingFile(parent: ctk.CTkToplevel) -> None:
    dialog = ctk.CTkToplevel(parent)
    dialog.geometry("550x100+600+400")
    dialog.title("USER INPUT")
    dialog.transient(parent)
    dialog.update()  
    dialog.grab_set()

    dialog.recording_label = ctk.CTkLabel(dialog, text=helper.FILE_QUESTION)
    dialog.recording_label.grid(row=0, column=0)
    dialog.entry = ctk.CTkEntry(dialog, placeholder_text="e.g: Recording_one")
    dialog.entry.grid(row=0, column=1, padx=10, pady=10)
  
    styler.StyleWindow(dialog)
    styler.StyleLabel(dialog.recording_label)
    
    dialog.entry.bind("<Return>", lambda event: Submit(entry=dialog.entry, window=dialog, parent_window=parent))


def StartRecording(parent: ctk.CTkToplevel) -> None:
    data_window = ctk.CTkToplevel(parent)
    data_window.geometry("600x200+750+350")
    data_window.title("DATA")
    data_window.transient(parent)
    data_window.update()  
    data_window.grab_set()
    
    data_window.label = ctk.CTkLabel(data_window, text=helper.DATA_PROMPT)
    data_window.label.grid(row=0, column=0)
    data_window.entry = ctk.CTkEntry(data_window)
    data_window.entry.grid(row=0, column=1, padx=10, pady=10)
    data_window.entry.focus_set() 

    styler.StyleLabel(data_window.label)
    styler.StyleWindow(data_window)

    camera_window = ctk.CTkToplevel(parent)
    camera_window.geometry("700x700")
    camera_window.title("CAMERA")
    camera_window.transient(parent)
    camera_window.update()  

    styler.StyleWindow(camera_window)

    camera_window.image_label = ctk.CTkLabel(camera_window, text=None)
    camera_window.image_label.grid(row=0, column=0)

    camera = helper.TurnCameraOn()
    displayCamera(camera=camera, window=camera_window, image_label=camera_window.image_label)

    data_window.entry.bind("<Return>", lambda event: GatherData(parent, data_window.entry, data_window, camera_window, camera))


def Submit(entry: ctk.CTkEntry, window: ctk.CTkToplevel, parent_window: ctk.CTkToplevel) -> None:
    user_input = entry.get()
   
    if helper.validate_input(user_input):
        window.destroy()
        helper.SetFolderName(user_input)
        StartRecording(parent_window)
    else:
        window.input_error_label = ctk.CTkLabel(window, text=helper.ERROR_INPUT)
        window.input_error_label.grid(row=1, column=0)
        entry.delete(0, ctk.END) 


def displayCamera(camera, window: ctk.CTkToplevel, image_label: ctk.CTkLabel) -> None:
    frame = helper.GetFrame(camera)
    video = ctk.CTkImage(light_image=frame, size=helper.VIDEO_WIDTH_LENGTH)
    image_label.configure(image=video)
    window.after(1, lambda: displayCamera(camera, window, image_label))


def GatherData(parent: ctk.CTkToplevel, entry: ctk.CTkEntry, data_window: ctk.CTkToplevel, camera_window: ctk.CTkToplevel, camera):
    data = entry.get()
    if data.strip() == "q":
        data_window.destroy()
        camera_window.destroy()
        helper.TurnOffCamera(camera)
        helper.CreateCSV()
        Consolidate(parent)
        return
    if hasattr(data_window, "input_error_label") and data_window.input_error_label:
        data_window.input_error_label.destroy()
        data_window.input_error_label = None
    try:
        data = float(data)
    except ValueError:
        data_window.input_error_label = ctk.CTkLabel(data_window, text=helper.ERROR_INPUT_TWO)
        data_window.input_error_label.grid(row=1, column=0)
        styler.StyleErrorLabel(data_window.input_error_label)
        entry.delete(0, ctk.END)
        return None
    
    helper.Snap(camera)
    helper.UpdateMoistureData(data)
    entry.focus_set()
    entry.delete(0, ctk.END)


def Consolidate(parent: ctk.CTkToplevel):
    dialog = ctk.CTkToplevel(parent)
    dialog.geometry("550x100+600+400")
    dialog.title("CONSOLIDATION")
    dialog.transient(parent)
    dialog.update() 
    dialog.grab_set()

    styler.StyleWindow(dialog)

    dialog.spinner_label = ctk.CTkLabel(dialog, text="|", font=("Arial", 24))
    dialog.spinner_label.grid(row=0, column=1, padx=20, pady=20)

    consolidating_label = ctk.CTkLabel(dialog, text=helper.CONSOLIDATION_LABEL)
    consolidating_label.grid(row=1, column=1)
    styler.StyleLabel(consolidating_label)

    for i in range(3):
        dialog.grid_rowconfigure(i, weight=1)
        dialog.grid_columnconfigure(i, weight=1)

    symbols = ["|", "/", "-", "\\"]
    def spin(i=0):
        dialog.spinner_label.configure(text=symbols[i % len(symbols)])
        dialog.spinner_label.after(100, lambda: spin(i + 1))
    spin()

    if helper.ConsolidateData():
        dialog.destroy()
        Roboflow(parent)
    else:
        dialog.error_label = ctk.CTkLabel(dialog, text=helper.CONSOLIDATION_ERROR_LABEL)
        dialog.error_label.grid(row=2, column=1)
        styler.StyleErrorLabel(dialog.error_label)


def Roboflow(parent: ctk.CTkToplevel):
    robo_window = ctk.CTkToplevel(parent)
    robo_window.geometry("550x100+600+400")
    robo_window.title("Data")
    robo_window.transient(parent)
    robo_window.update()  
    robo_window.grab_set()

    styler.StyleWindow(robo_window)

    robo_window.label = ctk.CTkLabel(robo_window, text=helper.ROBOFLOW_UPLOAD_LABEL)
    robo_window.label.grid(row=0, column=1)
    styler.StyleLabel(robo_window.label)

    helper.upload_data()

    
    






    

    






    
