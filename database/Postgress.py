import subprocess
import sys
import ctypes

SERVICE_NAME = "PostgreSQL-16"
DATA_DIR = r"C:\Program Files\PostgreSQL\16\data"

def run_command(command):
    """Execute a command and return its output."""
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    return process.stdout, process.stderr

def start_service():
    """Start the PostgreSQL service."""
    print("Starting PostgreSQL service...")
    stdout, stderr = run_command(f"net start {SERVICE_NAME}")
    if stderr:
        print(f"Error starting service: {stderr}")
    else:
        print(stdout)

def stop_service():
    """Stop the PostgreSQL service."""
    print("Stopping PostgreSQL service...")
    stdout, stderr = run_command(f"net stop {SERVICE_NAME}")
    if stderr:
        print(f"Error stopping service: {stderr}")
    else:
        print(stdout)

def set_service_startup_type(start_type):
    """Set the PostgreSQL service to a specified startup type (e.g., demand)."""
    print(f"Setting PostgreSQL service startup type to {start_type}...")
    command = f"sc config {SERVICE_NAME} start= {start_type}"
    stdout, stderr = run_command(command)
    if stderr:
        print(f"Error setting startup type: {stderr}")
    else:
        print(stdout)

def is_admin():
    """Check if the script is run as administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    """Re-run the script with administrator privileges."""
    script = sys.argv[0]
    params = ' '.join(sys.argv[1:])
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f"{script} {params}", None, 1)
    except Exception as e:
        print(f"Failed to elevate privileges: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage PostgreSQL service")
    parser.add_argument('action', choices=['start', 'stop', 'set'], help="Action to perform")
    parser.add_argument('--startup-type', choices=['auto', 'demand', 'disabled'], help="Set the startup type (only for 'set' action)")

    args = parser.parse_args()

    if not is_admin():
        run_as_admin()
    else:
        if args.action == 'start':
            start_service()
        elif args.action == 'stop':
            stop_service()
        elif args.action == 'set':
            if args.startup_type:
                set_service_startup_type(args.startup_type)
            else:
                print("Error: --startup-type argument is required for 'set' action")
