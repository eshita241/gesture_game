import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class ModernGameLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window settings
        self.setWindowTitle('mostalazikil')
        self.setFixedSize(400, 7000)
        
        # Set yellow background
        self.setStyleSheet("QMainWindow { background-color: #FFE135; }")
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # # Add Image
        # image_label = QLabel(self)
        # pixmap = QPixmap("C:\\Users\\shamb\\Downloads\\VIT2\\code\\project\\gesture_game\\launcher\\LAUNCH.jpg")  # Replace with the correct path to your image
        # image_label.setPixmap(pixmap)
        # image_label.setAlignment(Qt.AlignCenter)
        # layout.addWidget(image_label)
        
        # Logo
        logo_label = QLabel("mostalazikil")
        logo_label.setFont(QFont("Space Grotesk", 16, QFont.Bold))
        logo_label.setStyleSheet("color: black;")
        layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        
        # Cyber text
        cyber_label = QLabel("cyber\npunk")
        cyber_label.setFont(QFont("Space Grotesk", 64, QFont.Bold))
        cyber_label.setStyleSheet("color: black;")
        layout.addWidget(cyber_label, alignment=Qt.AlignLeft)
        
        # Future text
        future_label = QLabel("LET'S BUILD\nTHE FUTURE")
        future_label.setFont(QFont("Space Grotesk", 24, QFont.Bold))
        future_label.setStyleSheet("color: black;")
        layout.addWidget(future_label, alignment=Qt.AlignLeft)
        
        # Subtitle
        subtitle = QLabel("LET'S BUILD A NEW UNIVERSE\nIN CYBERPUNK 2077 AND\nEXPLORE THE FUTURE.")
        subtitle.setFont(QFont("Space Grotesk", 12))
        subtitle.setStyleSheet("color: black;")
        layout.addWidget(subtitle, alignment=Qt.AlignLeft)
        
        # Game buttons
        button_style = """
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 20px;
                padding: 10px;
                min-width: 100px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """
        
        self.krunker_btn = QPushButton("Launch Krunker.io")
        self.krunker_btn.setStyleSheet(button_style)
        
        self.subway_btn = QPushButton("Launch Subway")
        self.subway_btn.setStyleSheet(button_style)

        self.hill_btn = QPushButton("Launch Hill Climbing")
        self.hill_btn.setStyleSheet(button_style)
        
        self.snake_btn = QPushButton("Launch Snake.io")
        self.snake_btn.setStyleSheet(button_style)
        
        layout.addWidget(self.krunker_btn)
        layout.addWidget(self.subway_btn)
        layout.addWidget(self.hill_btn)
        layout.addWidget(self.snake_btn)
        
        # Status bar
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: black;")
        layout.addWidget(self.status_label)
        
        # Add stretch to push content to the top
        layout.addStretch()

    def launch_krunker(self):
        """Launch the Krunker game."""
        script_path = os.path.join(os.path.dirname(__file__), 'krunker.py')
        krunker_client_path = r"C:/Users/shamb/AppData/Local/Figma/Figma.exe"
        try:
            subprocess.Popen(['python', script_path])
            subprocess.Popen([krunker_client_path])
            self.status_label.setText("Status: Launching Krunker...")
        except Exception as e:
            self.status_label.setText(f"Status: Error - {str(e)}")

    def launch_subway(self):
        """Launch the Subway game."""
        script_path = os.path.join(os.path.dirname(__file__), 'subway.py')
        subway_path = ""
        try:
            subprocess.Popen(['python', script_path])
            subprocess.Popen([subway_path])
            self.status_label.setText("Status: Launching Subway...")
        except Exception as e:
            self.status_label.setText(f"Status: Error - {str(e)}")
    
    def launch_hill(self):
        """Launch the Subway game."""
        script_path = os.path.join(os.path.dirname(__file__), 'hill_climbing.py')
        try:
            subprocess.Popen(['python', script_path])
            self.status_label.setText("Status: Launching Subway...")
        except Exception as e:
            self.status_label.setText(f"Status: Error - {str(e)}")

    def launch_snake(self):
        """Launch the Subway game."""
        script_path = os.path.join(os.path.dirname(__file__), 'krunker.py')
        try:
            subprocess.Popen(['python', script_path])
            self.status_label.setText("Status: Launching Subway...")
        except Exception as e:
            self.status_label.setText(f"Status: Error - {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = ModernGameLauncher()
    
    # Connect button signals to their respective methods
    launcher.krunker_btn.clicked.connect(launcher.launch_krunker)
    launcher.subway_btn.clicked.connect(launcher.launch_subway)
    launcher.hill_btn.clicked.connect(launcher.launch_hill)
    launcher.snake_btn.clicked.connect(launcher.launch_snake)

    # Show the launcher window
    launcher.show()
    
    # Start the application event loop
    sys.exit(app.exec_())
