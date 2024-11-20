import subprocess
from pathlib import Path
import shutil

class Deployer:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.build_dir = self.root_dir / 'build'

    def build(self):
        """Build the project"""
        # Clean build directory
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        self.build_dir.mkdir()

        # Generate sites
        subprocess.run(['python', 'main.py'])

        # Optimize assets
        subprocess.run(['python', 'scripts/optimize_assets.py'])

    def deploy(self, environment='staging'):
        """Deploy the project"""
        self.build()

        if environment == 'staging':
            # Deploy to staging server
            subprocess.run(['rsync', '-avz', 'build/', 'user@staging-server:/var/www/'])
        elif environment == 'production':
            # Deploy to production server
            subprocess.run(['rsync', '-avz', 'build/', 'user@production-server:/var/www/'])

if __name__ == "__main__":
    deployer = Deployer()
    deployer.deploy('staging')

# Update deployment configuration
DEPLOY_CONFIG = {
    'author': 'reconsumeralization',
    'email': 'reconsumeralization@gmail.com',
    'repository': 'https://github.com/reconsumeralization/hw-websites.git'
}
