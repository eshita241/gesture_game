import sys
import subprocess
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QGridLayout, QMainWindow, QFrame, QHBoxLayout)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize

class ModernLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('⚡ SYSTEM APPLICATIONS ⚡')
        screen = QApplication.desktop().screenGeometry()
        width = int(screen.width() * 0.8)
        height = int(screen.height() * 0.8)
        self.setGeometry(int(screen.width()*0.1), int(screen.height()*0.1), width, height)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a14;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #0a0a14;
                border-right: 2px solid #00fff5;
                margin: 10px;
            }
        """)
        left_layout = QVBoxLayout()
        
        image_label = QLabel()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'img.png')
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(int(width*0.3), height, Qt.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(image_label)
        left_panel.setLayout(left_layout)
        left_panel.setFixedWidth(int(width*0.3))
        main_layout.addWidget(left_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout()

        header = QLabel('SYSTEM APPLICATIONS')
        header.setFont(QFont('Arial', 32, QFont.Bold))
        header.setStyleSheet("""
            color: #00fff5;
            padding: 20px;
            margin: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(header)

        grid = QGridLayout()
        grid.setSpacing(20)

        apps = [
            ('TERMINAL//CMD', 'cmd.exe', os.path.join(script_dir, 'image.png'), '#ff003c'),
            ('CALC//SYS', 'calc.exe', os.path.join(script_dir, 'image.png'), '#17b978'),
            ('TEXT//EDIT', 'notepad.exe', 'text_bg.png', '#00fff5'),
            ('PAINT//PRO', 'mspaint.exe', 'paint_bg.png', '#ff6b6b'),
            ('NET//BROWSE', 'chrome.exe', 'browser_bg.png', '#4e00ff'),
            ('FILE//SYS', 'explorer.exe', 'files_bg.png', '#00d8d8')
        ]

        for idx, (app_name, command, bg_image, color) in enumerate(apps):
            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    border: 2px solid {color};
                    border-radius: 10px;
                    background-color: #0a0a14;
                    min-height: 150px;
                }}
            """)
            
            button = QPushButton(app_name)
            button.setFont(QFont('Arial', 14, QFont.Bold))
            button.setMinimumSize(180, 130)
            button.setStyleSheet(f"""
                QPushButton {{
                    color: {color};
                    border: none;
                    border-radius: 8px;
                    padding: 15px;
                    text-align: center;
                    background-color: transparent;
                }}
                QPushButton:hover {{
                    background-color: rgba(0, 0, 0, 0.5);
                    border: 2px solid {color};
                }}
            """)
            button.clicked.connect(lambda checked, cmd=command: self.launch_app(cmd))
            
            layout = QVBoxLayout(frame)
            layout.addWidget(button)
            grid.addWidget(frame, idx//2, idx%2)

        right_layout.addLayout(grid)

        status = QLabel('SYSTEM STATUS: READY | SELECT APPLICATION TO LAUNCH')
        status.setStyleSheet("""
            color: #00fff5;
            padding: 10px;
            font-size: 14px;
        """)
        status.setAlignment(Qt.AlignLeft)
        right_layout.addWidget(status)

        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)

    def launch_app(self, app_command):
        try:
            subprocess.Popen(app_command)
        except Exception as e:
            self.statusBar().showMessage(f"ERROR: {str(e)}", 3000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModernLauncher()
    ex.show()
    sys.exit(app.exec_())
