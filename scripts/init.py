import os
import subprocess
import venv

def initialize_project():
    """Initialize the project with virtual environment and dependencies"""
    print("Initializing project...")

    # Create virtual environment
    venv.create('venv', with_pip=True)

    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_script = 'venv\\Scripts\\activate.bat'
        pip_path = 'venv\\Scripts\\pip.exe'
    else:  # Unix/Linux
        activate_script = 'venv/bin/activate'
        pip_path = 'venv/bin/pip'

    # Install requirements
    subprocess.run([pip_path, 'install', '-r', 'requirements.txt'])

    # Run setup and organization scripts
    subprocess.run(['python', 'setup.py'])
    subprocess.run(['python', 'cleanup.py'])

    print("Project initialized successfully!")

if __name__ == "__main__":
    initialize_project()
