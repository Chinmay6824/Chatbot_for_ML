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
        logging.FileHandler('simple_run.log'),
        logging.StreamHandler()
    ]
)

def check_dependencies():
    """Check if Flask is installed."""
    try:
        import flask
        print("Flask is already installed.")
        return True
    except ImportError:
        print("Flask is not installed. Attempting to install...")
        
        # Try different installation methods
        success = False
        
        # Method 1: Try using the current Python's pip
        try:
            print("Method 1: Using current Python's pip...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
            print("Flask installed successfully.")
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
                    subprocess.check_call(['pip', 'install', 'flask'])
                else:
                    subprocess.check_call(['pip3', 'install', 'flask'])
                print("Flask installed successfully.")
                success = True
            except subprocess.CalledProcessError as e:
                print(f"Method 2 failed: {e}")
            except Exception as e:
                print(f"Method 2 failed with unexpected error: {e}")
        
        if not success:
            print("\nAutomatic installation failed. Please install Flask manually:")
            print("pip install flask")
            return False
    
    return True

def run_simple_server():
    """Run the simple server directly."""
    try:
        print("=" * 50)
        print("Starting Simple ML Chatbot")
        print("=" * 50)
        print(f"Using Python: {sys.executable}")
        print(f"Python version: {platform.python_version()}")
        
        # Import and run the server directly
        from simple_server import app
        print("Server will be available at http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
        
    except ImportError as e:
        logging.error(f"Import error: {e}")
        print(f"Error importing Flask: {e}")
        return False
    except Exception as e:
        logging.error(f"Error running server: {e}")
        print(f"Error running server: {e}")
        return False

if __name__ == "__main__":
    # Check if Flask is installed
    if not check_dependencies():
        print("Failed to install Flask. Exiting...")
        sys.exit(1)
    
    # Run the simple server
    run_simple_server() 