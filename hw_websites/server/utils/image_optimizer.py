from PIL import Image
import os
from io import BytesIO
import requests

class ImageOptimizer:
    def __init__(self, quality=85):
        self.quality = quality
        self.sizes = {
            'thumbnail': (150, 150),
            'medium': (300, 300),
            'large': (800, 800)
        }

    def optimize_image(self, image_path, output_dir):
        """Optimize image and create different sizes"""
        img = Image.open(image_path)

        # Generate different sizes
        variants = {}
        for size_name, dimensions in self.sizes.items():
            resized = img.copy()
            resized.thumbnail(dimensions)

            # Save optimized version
            output_path = os.path.join(
                output_dir,
                f"{os.path.splitext(os.path.basename(image_path))[0]}_{size_name}.webp"
            )
            resized.save(output_path, 'WEBP', quality=self.quality)
            variants[size_name] = output_path

        return variants
