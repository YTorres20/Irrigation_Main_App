import platform
import sys 
import shutil
import subprocess
import cv2
import os 


class SystemManager:
    """
    Manages system-specific setup for camera and terminal control.

    - Detects the OS (Linux, Windows, MacOS)  
    - Installs missing dependencies if needed (wmctrl on Linux, pywin32 on Windows)  
    - Provides a method to bring a terminal window to the front  
    - Provides a method to determine the correct camera device and OpenCV capture backend
    """
    def __init__(self):
        self.system_name = platform.system()

        if self.system_name == "Linux":
            if shutil.which("wmctrl") is None:
                print("\nwmctrl is not installed. Installing...\n")
                subprocess.run(["sudo","apt", "install", "-y", "wmctrl"])
                print("\nInstallation complete.\n")
            else: 
                print("\nwmctrl is installed.\n")
        elif self.system_name == "Windows":
            try:
                import win32gui, win32con
            except ImportError:
                print("\npywin32 not found. Installing...\n")
                subprocess.run([sys.executable,"-m","pip","install","pywin32"])
                print("\nInstallation Complete.\n")

    def bring_terminal_to_front(self):
        if self.system_name == "Linux":

            terminals = ["gnome-terminal", "xterm", "konsole", "tilix", "xfce4-terminal"]

            for terminal in terminals:
                result = subprocess.run(["wmctrl", "-a", terminal])
                if result.returncode == 0:
                    print("\nTerminal Brought to the Front.\n")
                    return 
            
        elif self.system_name == "Windows":
            import win32gui, win32con

            terminals = ["Command Prompt", "cmd.exe","PowerShell", "Windows PowerShell", "Terminal", "Windows Terminal"]

            found = []

            def callback(window,extra):
                title = win32gui.GetWindowText(window)

                for name in terminals:
                    if name.lower() in title.lower():
                        extra.append(window)
                        break

                return True # keep enumerating

            win32gui.EnumWindows(callback, found)

            if not found: 
                print("\nUnknown Terminal...Please check code terminals in system.py\n")
                return
        
            terminal = found[0]

            win32gui.ShowWindow(terminal,win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(terminal)
            print("\nTerminal brought to the front.\n")

        elif self.system_name== "Darwin":
            terminals = ["Terminal", "iTerm", "iTerm2"]

            for terminal in terminals:
                try:
                    result = subprocess.run(["osascript", "-e", f'tell application "{terminal}" to activate'],  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                    if result.returncode == 0:
                        print(f"\n{terminal} brought to the front.\n")
                        return

                except Exception:
                 continue

        print("\nUnknown Terminal...Please check code terminals in system.py\n")

    def get_camera_device(self):
        if self.system_name == "Linux":
            devices = [f"/dev/{d}" for d in os.listdir("/dev") if d.startswith("video")]
            if not devices:
                print("\n❌ No camera device found under /dev/\n")
                return 0, cv2.CAP_V4L2
            return devices[0], cv2.CAP_V4L2
    
        elif self.system_name == "Windows":
         return 0, cv2.CAP_DSHOW
    
        elif self.system_name == "Darwin":
            return 0, cv2.CAP_AVFOUNDATION
    
        else:
            return 0, cv2.CAP_ANY

