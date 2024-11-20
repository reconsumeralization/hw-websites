import os
import shutil
from PIL import Image

class AssetManager:
    def __init__(self, base_dir='assets'):
        self.base_dir = base_dir
        self.image_sizes = {
            'thumbnail': (150, 150),
            'medium': (800, 600),
            'large': (1920, 1080)
        }

    def setup_directories(self, site_name):
        """Create necessary directories for a site"""
        dirs = [
            f'{site_name}/images',
            f'{site_name}/css',
            f'{site_name}/js',
            f'{site_name}/fonts'
        ]

        for dir_path in dirs:
            full_path = os.path.join(self.base_dir, dir_path)
            os.makedirs(full_path, exist_ok=True)

    def optimize_images(self, site_name):
        """Optimize all images for a site"""
        image_dir = os.path.join(self.base_dir, f'{site_name}/images')
        optimized_dir = os.path.join(self.base_dir, f'{site_name}/images/optimized')
        os.makedirs(optimized_dir, exist_ok=True)

        for filename in os.listdir(image_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(image_dir, filename)
                self._optimize_image(image_path, optimized_dir)

    def _optimize_image(self, image_path, output_dir):
        """Optimize a single image"""
        img = Image.open(image_path)
        filename = os.path.basename(image_path)
        name, ext = os.path.splitext(filename)

        # Create different sizes
        for size_name, dimensions in self.image_sizes.items():
            resized = img.copy()
            resized.thumbnail(dimensions)
            output_path = os.path.join(
                output_dir,
                f'{name}_{size_name}{ext}'
            )
            resized.save(output_path, optimize=True, quality=85)
