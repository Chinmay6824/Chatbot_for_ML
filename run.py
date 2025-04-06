#!/usr/bin/env python
"""
Script to run both the frontend and backend of the ML Chatbot application.
This script starts both servers in separate processes.
"""

import os
import subprocess
import sys
import time
import webbrowser
from threading import Timer
import socket

def check_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def open_browser():
    """Open the browser to the application URL"""
    # Check if the server is actually running before opening browser
    if check_port_in_use(5000):
        print("Server detected on port 5000, opening browser...")
        webbrowser.open('http://localhost:5000')
    else:
        print("WARNING: Server not detected on port 5000, browser won't be opened")

def main():
    """Main function to start the server"""
    try:
        # Check if port 5000 is already in use
        if check_port_in_use(5000):
            print("ERROR: Port 5000 is already in use. Please close the application using this port and try again.")
            return
            
        # Use the full path to Python
        python_executable = r"C:\Users\Asus\AppData\Local\Programs\Python\Python312\python.exe"
        
        # Check if the Python executable exists
        if not os.path.exists(python_executable):
            print(f"ERROR: Python executable not found at {python_executable}")
            print("Please update the python_executable path in run.py")
            return
            
        # Get the absolute path to ml_chatbot_intents.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(script_dir, 'ml_chatbot_intents.py')
        
        # Check if the file exists
        if not os.path.exists(app_path):
            print(f"ERROR: Could not find {app_path}")
            print("Current directory contains:")
            for file in os.listdir(script_dir):
                print(f"  - {file}")
            return
        
        print("Starting ML Chatbot server...")
        print(f"Using Python: {python_executable}")
        print(f"Running script: {app_path}")
        
        # Start the server using the current Python interpreter with output capture
        process = subprocess.Popen(
            [python_executable, app_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Give the server a moment to start and check for immediate errors
        print("Waiting for server to start...")
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is not None:
            # Process has already terminated
            stdout, stderr = process.communicate()
            print("ERROR: Server failed to start!")
            print("\nSTDOUT:")
            print(stdout)
            print("\nSTDERR:")
            print(stderr)
            return
            
        # Start a thread to monitor the process output
        def monitor_output():
            while True:
                stdout_line = process.stdout.readline()
                if stdout_line:
                    print(f"SERVER: {stdout_line.strip()}")
                stderr_line = process.stderr.readline()
                if stderr_line:
                    print(f"SERVER ERROR: {stderr_line.strip()}")
                if process.poll() is not None:
                    break
                    
        import threading
        output_thread = threading.Thread(target=monitor_output, daemon=True)
        output_thread.start()
        
        # Open the browser after a short delay
        Timer(3, open_browser).start()
        
        print("\nML Chatbot is running!")
        print("Server: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        
        # Wait for the process to complete (which it won't unless stopped)
        process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
        if 'process' in locals() and process:
            process.terminate()
        print("Server stopped")
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'process' in locals() and process:
            process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main() 