import unittest
from hw_websites.server.generate_pages import EnhancedPageGenerator

class TestPageGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = EnhancedPageGenerator()

    def test_seo_content_generation(self):
        content = "Test content about road construction"
        meta_description = self.generator.seo_generator.generate_meta_description(content)
        self.assertLessEqual(len(meta_description), 160)

    def test_image_optimization(self):
        test_image = "test_image.jpg"
        optimized = self.generator.image_optimizer.optimize_image(test_image, "output")
        self.assertIn('thumbnail', optimized)
        self.assertIn('medium', optimized)
        self.assertIn('large', optimized)
