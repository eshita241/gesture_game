from launcher_ui import GameLauncherUI
import tkinter as tk
import subprocess
import os

def launch_krunker():
    script_path = os.path.join(os.path.dirname(__file__), 'krunker.py')
    subprocess.Popen(['python', script_path])
    ui.set_status("Launching Krunker...")

def launch_subway():
    script_path = os.path.join(os.path.dirname(__file__), 'subway.py')
    subprocess.Popen(['python', script_path])
    ui.set_status("Launching Subway...")

root = tk.Tk()
ui = GameLauncherUI(root)
ui.set_krunker_command(launch_krunker)
ui.set_subway_command(launch_subway)
root.mainloop()