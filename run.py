import subprocess
import sys
import os

def run_backend():
    return subprocess.Popen([
        sys.executable,
        "-m",
        "uvicorn",
        "backend.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload",
        "--reload-include=.*",
    ])

def run_frontend():
    return subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501"])

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Starting FAQ Chatbot...")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:8501")
    
    backend_proc = run_backend()
    frontend_proc = run_frontend()
    
    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend_proc.terminate()
        frontend_proc.terminate()