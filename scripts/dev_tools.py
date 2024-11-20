import subprocess
from pathlib import Path

class DevTools:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent

    def run_tests(self):
        """Run all tests"""
        subprocess.run(['pytest', 'tests'])

    def check_code_quality(self):
        """Run code quality checks"""
        subprocess.run(['flake8', 'server'])
        subprocess.run(['black', 'server'])
        subprocess.run(['mypy', 'server'])

    def generate_docs(self):
        """Generate documentation"""
        subprocess.run(['sphinx-build', '-b', 'html', 'docs/source', 'docs/build'])

if __name__ == "__main__":
    tools = DevTools()
    tools.check_code_quality()
    tools.run_tests()
    tools.generate_docs()
