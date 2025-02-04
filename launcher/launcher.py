from PyQt5.QtWidgets import QApplication, QMainWindow
from launcher_ui import ModernGameLauncher
import subprocess
import os
import sys

def launch_krunker():
    script_path = os.path.join(os.path.dirname(__file__), 'krunker.py')
    subprocess.Popen(['python', script_path])
    ui.set_status("Launching Krunker...")

def launch_subway():
    script_path = os.path.join(os.path.dirname(__file__), 'subway.py')
    subprocess.Popen(['python', script_path])
    ui.set_status("Launching Subway...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = ModernGameLauncher()
    main_window.setCentralWidget(ui)

    # Set commands for the buttons
        # Connect button signals to their respective methods
    ui.krunker_btn.clicked.connect(launch_krunker)
    ui.subway_btn.clicked.connect(launch_subway)


    main_window.show()
    sys.exit(app.exec_())