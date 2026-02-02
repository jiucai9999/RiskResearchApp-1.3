import sys
import subprocess
import threading
import time
from PySide6.QtWidgets import QApplication
import webview

def run_streamlit():
    subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run",
            "app/streamlit_app.py",
            "--server.headless=true",
            "--server.port=8501",
            "--browser.gatherUsageStats=false"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

if __name__ == "__main__":
    threading.Thread(target=run_streamlit, daemon=True).start()
    time.sleep(2)

    app = QApplication(sys.argv)
    webview.create_window(
        "多品种交易风控与研究系统",
        "http://127.0.0.1:8501",
        width=1200,
        height=800
    )
    webview.start()
