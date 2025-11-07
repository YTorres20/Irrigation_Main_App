import customtkinter as ctk


PRIMARY_COLOR = "#1E90FF"
TEXT_COLOR = "black"
HOVER_COLOR = "#104E8B"
FONT_TITLE = ("Arial", 40)
FONT_MEDIUM = ("Arial", 12)
BACK_GROUND_COLOR = "black"
ERROR_TEXT_COLOR = "red"



def StyleButton(button: ctk.CTkButton) -> None:
 
    button.configure(
        fg_color=PRIMARY_COLOR,
        text_color=TEXT_COLOR,
        hover_color=HOVER_COLOR,
        corner_radius=10,
        font=FONT_MEDIUM
        
    )

def StyleMainLabel(label: ctk.CTkLabel) -> None:
    
    label.configure(
        text_color=PRIMARY_COLOR,
        font=FONT_TITLE
    )

def StyleWindow(window: ctk.CTkToplevel) -> None:
    window.configure(
        #fg_color=BACK_GROUND_COLOR
    )

def StyleLabel(label: ctk.CTkLabel) -> None:
    
    label.configure(
        text_color=TEXT_COLOR,
	    font=FONT_MEDIUM

    )

def StyleErrorLabel(label: ctk.CTkLabel) -> None:
 
    label.configure(
        text_color=ERROR_TEXT_COLOR,
        font=FONT_MEDIUM
    )

