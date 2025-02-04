import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QLabel, QPushButton, QFrame, QHBoxLayout)
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap
from PyQt5.QtCore import Qt, QSize

class CyberLauncher(QMainWindow):
    def _init_(self):
        super()._init_()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cyber Launcher')
        self.setFixedSize(400, 600)  # Increased vertical size
        
        # Set main background color
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFD62E;
            }
        """)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Top section with brand and menu
        top_section = QHBoxLayout()
        
        # Brand text
        brand = QLabel('mostafa\nzidi')
        brand.setStyleSheet("""
            QLabel {
                color: #000;
                font-size: 16px;
                font-weight: 500;
                padding: 0;
            }
        """)
        top_section.addWidget(brand)

        # Menu toggle
        menu_container = QWidget()
        menu_container.setFixedSize(24, 18)
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setSpacing(4)
        
        for _ in range(3):
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("""
                QFrame {
                    background-color: #000;
                    border: none;
                    min-height: 2px;
                    max-height: 2px;
                }
            """)
            menu_layout.addWidget(line)

        top_section.addWidget(menu_container, alignment=Qt.AlignRight | Qt.AlignTop)
        layout.addLayout(top_section)

        # Add spacing
        layout.addSpacing(40)

        # Cyber text
        cyber_text = QLabel('CYBER\nPUNK')
        cyber_text.setStyleSheet("""
            QLabel {
                color: #000;
                font-size: 72px;
                font-weight: 700;
                letter-spacing: -2px;
                line-height: 0.8;
            }
        """)
        layout.addWidget(cyber_text)

        # Add spacing
        layout.addSpacing(40)

        # Title
        title = QLabel("LET'S BUILD THE FUTURE")
        title.setStyleSheet("""
            QLabel {
                color: #000;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("LET'S BUILD A NEW UNIVERSE IN CYBERPUNK-2077 AND EXPLORE THE FUTURE.")
        subtitle.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 14px;
                line-height: 1.4;
            }
        """)
        subtitle.setWordWrap(True)
        subtitle.setFixedWidth(280)
        layout.addWidget(subtitle)

        # Add spacing
        layout.addSpacing(20)

        # Join button
        join_button = QPushButton('Join')
        join_button.setFixedSize(100, 36)
        join_button.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                color: #000;
                border-radius: 18px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        layout.addWidget(join_button)

        # Character image placeholder
        character_image = QLabel()
        script_dir = os.path.dirname(os.path.abspath(_file_))
        image_path = os.path.join(script_dir, 'character.png')  # Replace with your image
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            character_image.setPixmap(pixmap.scaled(
                320, 300, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            ))
        character_image.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        layout.addWidget(character_image)

        # Add remaining space to bottom
        layout.addStretch()

def load_fonts():
    """Load custom fonts and return the font family name"""
    font_path = os.path.join(os.path.dirname(_file_), 'SpaceGrotesk-Bold.ttf')
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id < 0:
        print("Warning: Error loading custom font, falling back to system font")
        return "Arial"
    else:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            return font_families[0]
        return "Arial"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Load and set default font
    default_font = load_fonts()
    app.setFont(QFont(default_font))
    
    ex = CyberLauncher()
    ex.show()
    sys.exit(app.exec_())