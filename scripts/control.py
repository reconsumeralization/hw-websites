import os
import shutil
import subprocess
from pathlib import Path

class ProjectController:
    def __init__(self):
        self.root_dir = Path(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
        self.hw_websites_dir = self.root_dir / 'hw_websites'
        self.backup_dir = self.root_dir / 'backups'
        self.temp_dir = self.root_dir / 'temp'

    def setup(self):
        """Initial project setup"""
        print("Setting up project structure...")

        # Run setup.py
        setup_script = self.root_dir / 'setup.py'
        subprocess.run(['python', str(setup_script)])

        # Create backup directory
        os.makedirs(self.backup_dir, exist_ok=True)
        print("Setup complete!")

    def backup(self, name="backup"):
        """Create a backup of the current state"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{name}_{timestamp}"
        backup_path = self.backup_dir / backup_name

        print(f"Creating backup: {backup_name}")
        shutil.copytree(self.hw_websites_dir, backup_path)
        print("Backup complete!")
        return backup_path

    def restore(self, backup_name=None):
        """Restore from a backup"""
        if backup_name is None:
            # Get most recent backup
            backups = sorted(self.backup_dir.glob('*'))
            if not backups:
                print("No backups found!")
                return
            backup_path = backups[-1]
        else:
            backup_path = self.backup_dir / backup_name
            if not backup_path.exists():
                print(f"Backup {backup_name} not found!")
                return

        print(f"Restoring from backup: {backup_path.name}")

        # Remove current hw_websites directory
        if self.hw_websites_dir.exists():
            shutil.rmtree(self.hw_websites_dir)

        # Restore from backup
        shutil.copytree(backup_path, self.hw_websites_dir)
        print("Restore complete!")

    def clean(self):
        """Clean up the project structure"""
        print("Cleaning project...")

        # Run cleanup.py
        cleanup_script = self.root_dir / 'cleanup.py'
        subprocess.run(['python', str(cleanup_script)])

        print("Clean complete!")

    def reset(self):
        """Reset project to initial state"""
        print("Resetting project...")

        # Remove hw_websites directory
        if self.hw_websites_dir.exists():
            shutil.rmtree(self.hw_websites_dir)

        # Run setup
        self.setup()
        print("Reset complete!")

    def list_backups(self):
        """List all available backups"""
        print("\nAvailable backups:")
        backups = sorted(self.backup_dir.glob('*'))
        for backup in backups:
            print(f"- {backup.name}")

    def init(self):
        """Initialize the project"""
        subprocess.run(['python', 'scripts/init.py'])

    def dev(self):
        """Run development tools"""
        subprocess.run(['python', 'scripts/dev_tools.py'])

    def deploy(self, environment='staging'):
        """Deploy the project"""
        subprocess.run(['python', 'scripts/deploy.py', environment])

    def monitor(self):
        """Start monitoring"""
        subprocess.run(['python', 'scripts/monitor.py'])

def main():
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description='Project Control Script')
    parser.add_argument('command', choices=['setup', 'backup', 'restore', 'clean', 'reset', 'list', 'init', 'dev', 'deploy', 'monitor'])
    parser.add_argument('--name', help='Name for backup or restore')

    args = parser.parse_args()
    controller = ProjectController()

    if args.command == 'setup':
        controller.setup()
    elif args.command == 'backup':
        controller.backup(args.name)
    elif args.command == 'restore':
        controller.restore(args.name)
    elif args.command == 'clean':
        controller.clean()
    elif args.command == 'reset':
        controller.reset()
    elif args.command == 'list':
        controller.list_backups()
    elif args.command == 'init':
        controller.init()
    elif args.command == 'dev':
        controller.dev()
    elif args.command == 'deploy':
        controller.deploy(args.name)
    elif args.command == 'monitor':
        controller.monitor()

if __name__ == "__main__":
    main()
