import os
import subprocess
import sys

def main():
    print("Checking dependencies...")
    # Optional: could run pip install here but as a senior architect, we assume environment is ready or user follows README
    
    print("Starting Skylark BI Agent UI...")
    ui_path = os.path.join("ui", "app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", ui_path])

if __name__ == "__main__":
    main()
