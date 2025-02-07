import subprocess
import os
import threading

def run_script(script_path):
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

def main():
    # Paths to the main.py scripts
    script1_path = os.path.join("..", "CauHinhChiBaoKyThuat", "main.py")
    script2_path = os.path.join("..", "ChiBaoKyThuat", "main.py")

    print("Running CauHinhChiBaoKyThuat/main.py...")
    run_script(script1_path)
    
    print("Running ChiBaoKyThuat/main.py...")
    run_script(script2_path)

if __name__ == "__main__":
    main()
