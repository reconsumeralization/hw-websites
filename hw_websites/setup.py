import os
import shutil

def organize_project():
    # Define source and destination paths
    src_root = os.path.abspath('.')
    dest_root = os.path.join(src_root, 'hw_websites')

    # Create destination directories if they don't exist
    directories = [
        'assets/css',
        'assets/fonts',
        'assets/images/hwroads.com',
        'assets/images/hwasphaltfl.com',
        'assets/js',
        'data',
        'server/templates',
        'server/utils',
        'tests'
    ]

    for directory in directories:
        os.makedirs(os.path.join(dest_root, directory), exist_ok=True)

    # Move utility files to server/utils
    util_files = [
        'asset_manager.py',
        'content_checker.py',
        'content_linker.py',
        'image_optimizer.py',
        'location_manager.py',
        'monitor.py',
        'performance_monitor.py',
        'review_generator.py',
        'schema_generator.py',
        'seo_content_generator.py'
    ]

    for file in util_files:
        src = os.path.join(dest_root, 'server', file)
        if os.path.exists(src):
            dest = os.path.join(dest_root, 'server', 'utils', file)
            print(f"Moving {src} to {dest}")
            shutil.move(src, dest)

    # Create __init__.py files if they don't exist
    init_locations = [
        os.path.join(dest_root, 'server'),
        os.path.join(dest_root, 'server', 'utils'),
        os.path.join(dest_root, 'tests')
    ]

    for location in init_locations:
        init_file = os.path.join(location, '__init__.py')
        if not os.path.exists(init_file):
            open(init_file, 'a').close()
            print(f"Created {init_file}")

    # Update imports in Python files
    python_files = []
    for root, _, files in os.walk(dest_root):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    for file_path in python_files:
        update_imports(file_path)

    print("Project structure organized successfully!")

def update_imports(file_path):
    """Update import statements in Python files"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update import statements
    content = content.replace(
        'from server.',
        'from hw_websites.server.'
    )
    content = content.replace(
        'from server import',
        'from hw_websites.server import'
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated imports in {file_path}")

if __name__ == "__main__":
    organize_project()
