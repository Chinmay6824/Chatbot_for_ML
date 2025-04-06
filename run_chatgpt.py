import os
import sys
import subprocess
import logging
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot_run.log'),
        logging.StreamHandler()
    ]
)

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = ['flask', 'flask-cors', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Attempting to install missing packages...")
        
        # Try different installation methods
        success = False
        
        # Method 1: Try using the current Python's pip
        try:
            print("Method 1: Using current Python's pip...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("All required packages installed successfully.")
            success = True
        except subprocess.CalledProcessError as e:
            print(f"Method 1 failed: {e}")
        except Exception as e:
            print(f"Method 1 failed with unexpected error: {e}")
        
        # Method 2: Try using pip directly if Method 1 failed
        if not success:
            try:
                print("Method 2: Using pip directly...")
                # On Windows, try pip.exe
                if platform.system() == 'Windows':
                    subprocess.check_call(['pip', 'install'] + missing_packages)
                else:
                    subprocess.check_call(['pip3', 'install'] + missing_packages)
                print("All required packages installed successfully.")
                success = True
            except subprocess.CalledProcessError as e:
                print(f"Method 2 failed: {e}")
            except Exception as e:
                print(f"Method 2 failed with unexpected error: {e}")
        
        # Method 3: Try using Python's pip with user flag
        if not success:
            try:
                print("Method 3: Using pip with --user flag...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user'] + missing_packages)
                print("All required packages installed successfully.")
                success = True
            except subprocess.CalledProcessError as e:
                print(f"Method 3 failed: {e}")
            except Exception as e:
                print(f"Method 3 failed with unexpected error: {e}")
        
        if not success:
            print("\nAutomatic installation failed. Please install the required packages manually:")
            print(f"pip install {' '.join(missing_packages)}")
            print("\nOr try running one of these commands:")
            print(f"python -m pip install {' '.join(missing_packages)}")
            print(f"python3 -m pip install {' '.join(missing_packages)}")
            print(f"pip3 install {' '.join(missing_packages)}")
            return False
    
    return True

def check_python_version():
    """Check if Python version is compatible."""
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print(f"Warning: This application requires Python 3.6 or higher. You are using Python {python_version.major}.{python_version.minor}")
        return False
    return True

def start_server():
    """Start the ChatGPT server."""
    try:
        print("Starting ML ChatGPT Bot server...")
        print("Server will be available at http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        
        # Run the server
        from chatgpt_server import app
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
        
    except ImportError as e:
        logging.error(f"Import error: {e}")
        print(f"Error importing required modules: {e}")
        print("Please make sure all dependencies are installed correctly.")
        return False
    except Exception as e:
        logging.error(f"Error starting server: {e}")
        print(f"Error starting server: {e}")
        return False
    
    return True

def manual_server_start():
    """Provide instructions for manual server start."""
    print("\nIf you continue to experience issues, try running the server directly:")
    print("1. Make sure Flask is installed: pip install flask flask-cors requests")
    print("2. Run the server directly: python chatgpt_server.py")
    print("\nAlternatively, you can try using a different Python installation.")

if __name__ == "__main__":
    print("=" * 50)
    print("ML ChatGPT Bot Server")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("Warning: Continuing with an unsupported Python version may cause issues.")
    
    # Print Python information
    print(f"Using Python: {sys.executable}")
    print(f"Python version: {platform.python_version()}")
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("Failed to install required dependencies automatically.")
        manual_server_start()
        sys.exit(1)
    
    # Start the server
    if not start_server():
        print("Failed to start the server.")
        manual_server_start()
        sys.exit(1) 