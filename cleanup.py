import os
import shutil

def cleanup_project():
    # Define paths
    root_dir = os.path.abspath('.')
    hw_websites_dir = os.path.join(root_dir, 'hw_websites')

    # Files to move from root to hw_websites
    root_files = [
        'setup.py',
        'main.py',
        '.gitignore',
        '.env'
    ]

    # Move files from root to hw_websites if they exist in both places
    for file in root_files:
        root_file = os.path.join(root_dir, file)
        hw_file = os.path.join(hw_websites_dir, file)

        if os.path.exists(root_file) and os.path.exists(hw_file):
            # Remove duplicate in hw_websites and move the root file
            os.remove(hw_file)
            shutil.move(root_file, hw_file)
            print(f"Moved {file} from root to hw_websites")
        elif os.path.exists(root_file):
            shutil.move(root_file, hw_file)
            print(f"Moved {file} to hw_websites")

    # Remove empty server/images directory if it exists
    server_images = os.path.join(hw_websites_dir, 'server', 'images')
    if os.path.exists(server_images) and not os.listdir(server_images):
        os.rmdir(server_images)
        print("Removed empty server/images directory")

    # Ensure all utility files are in the correct location
    utils_dir = os.path.join(hw_websites_dir, 'server', 'utils')
    server_dir = os.path.join(hw_websites_dir, 'server')

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
        src = os.path.join(server_dir, file)
        dest = os.path.join(utils_dir, file)
        if os.path.exists(src) and not os.path.exists(dest):
            shutil.move(src, dest)
            print(f"Moved {file} to utils directory")

    print("Project cleanup completed successfully!")

if __name__ == "__main__":
    cleanup_project()
