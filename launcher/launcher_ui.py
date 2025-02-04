import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class GameLauncherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.geometry("400x300")
        
        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=10, font=('Helvetica', 12))
        style.configure("TFrame", background="#f0f0f0")
        
        # Main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="Game Launcher", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=20)
        
        # Buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Game buttons
        self.krunker_btn = ttk.Button(
            button_frame,
            text="Launch Krunker",
            width=25
        )
        self.krunker_btn.pack(pady=10)
        
        self.subway_btn = ttk.Button(
            button_frame,
            text="Launch Subway",
            width=25
        )
        self.subway_btn.pack(pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            font=('Helvetica', 10)
        )
        self.status_bar.pack(side=tk.BOTTOM, pady=10)
        
    def set_status(self, message):
        self.status_var.set(message)
        
    def set_krunker_command(self, command):
        self.krunker_btn.config(command=command)
        
    def set_subway_command(self, command):
        self.subway_btn.config(command=command)