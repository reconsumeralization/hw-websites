import subprocess
import sys

def install_requirements():
    """Install all required packages"""
    requirements = [
        'psutil',
        'flask',
        'flask-mail',
        'wtforms',
        'pillow',
        'folium',
        'geocoder',
        'geopy',
        'beautifulsoup4',
        'spacy',
        'yake',
        'transformers',
        'language-tool-python',
        'textblob',
        'requests',
        'python-dotenv'
    ]

    print("Installing required packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")

    # Install spaCy English language model
    print("Installing spaCy English language model...")
    subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])

    print("Installation complete!")

if __name__ == "__main__":
    install_requirements()
