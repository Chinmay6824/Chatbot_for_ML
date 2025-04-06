import subprocess
import sys
import time

def main():
    """Simple script to run the Flask server and show all output"""
    print("Testing Flask installation...")
    try:
        # Check if Flask is installed
        import flask
        print(f"Flask is installed (version {flask.__version__})")
    except ImportError:
        print("ERROR: Flask is not installed. Please install it with:")
        print("pip install flask flask-cors")
        return

    print("\nTrying to run a simple test server...")
    try:
        # Run the test server
        process = subprocess.Popen(
            [sys.executable, "test_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            universal_newlines=True
        )
        
        # Wait for a bit to see if it starts
        time.sleep(3)
        
        # Check if it's still running
        if process.poll() is None:
            print("Test server started successfully!")
            print("You should be able to access it at http://localhost:5000")
            print("Press Ctrl+C to stop the test server")
            
            # Show output
            while True:
                stdout_line = process.stdout.readline()
                if stdout_line:
                    print(f"SERVER: {stdout_line.strip()}")
                stderr_line = process.stderr.readline()
                if stderr_line:
                    print(f"SERVER ERROR: {stderr_line.strip()}")
                if process.poll() is not None:
                    break
        else:
            # Process has already terminated
            stdout, stderr = process.communicate()
            print("ERROR: Test server failed to start!")
            print("\nSTDOUT:")
            print(stdout)
            print("\nSTDERR:")
            print(stderr)
    except KeyboardInterrupt:
        print("\nStopping test server...")
        if 'process' in locals() and process:
            process.terminate()
        print("Test server stopped")
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'process' in locals() and process:
            process.terminate()

if __name__ == "__main__":
    main() 