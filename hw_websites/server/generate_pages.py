import os
from hw_websites.server.utils.content_linker import ContentLinker
from hw_websites.server.utils.seo_content_generator import SEOContentGenerator
from hw_websites.server.utils.image_optimizer import ImageOptimizer
from hw_websites.server.utils.schema_generator import SchemaGenerator
from hw_websites.server.utils.performance_monitor import PerformanceMonitor
from hw_websites.server.utils.content_checker import ContentQualityChecker
from hw_websites.server.utils.location_manager import LocationManager
from hw_websites.server.utils.review_generator import ReviewGenerator

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def generate_html_file(filepath, title, site_name, city_name, content=None):
    if content is None:
        content = f"<h1>{title}</h1>"

    # Define site-specific styles
    if site_name == 'hwroads.com':
        header_class = "bg-blue-800 text-white"
        nav_class = "bg-blue-700 text-white"
        button_class = "bg-blue-600 text-white"
        footer_class = "bg-blue-800 text-white"
        stylesheet = "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
    elif site_name == 'hwasphaltfl.com':
        header_class = "bg-gray-800 text-white"
        nav_class = "bg-gray-700 text-white"
        button_class = "bg-yellow-500 text-gray-900"
        footer_class = "bg-gray-800 text-white"
        stylesheet = "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
    else:
        # Default styles
        header_class = "bg-blue-800 text-white"
        nav_class = "bg-blue-700 text-white"
        button_class = "bg-blue-600 text-white"
        footer_class = "bg-blue-800 text-white"
        stylesheet = "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"

    # Define structured data
    structured_data = f"""
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "{'HW Roads' if site_name == 'hwroads.com' else 'HW Asphalt FL'}",
        "image": "/assets/images/logo.png",
        "@id": "",
        "url": "https://{'hwroads.com' if site_name == 'hwroads.com' else 'hwasphaltfl.com'}",
        "telephone": "(555) {'123-4567' if site_name == 'hwroads.com' else '987-6543'}",
        "address": {{
            "@type": "PostalAddress",
            "streetAddress": "123 Main Street",
            "addressLocality": "{city_name}",
            "addressRegion": "FL",
            "postalCode": "33101",
            "addressCountry": "US"
        }},
        "geo": {{
            "@type": "GeoCoordinates",
            "latitude": "25.7617",
            "longitude": "-80.1918"
        }},
        "openingHoursSpecification": {{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday"
            ],
            "opens": "08:00",
            "closes": "18:00"
        }},
        "sameAs": [
            "https://www.facebook.com/yourpage",
            "https://twitter.com/yourprofile",
            "https://www.linkedin.com/company/yourcompany"
        ]
    }}
    </script>
    """

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{'HW Roads' if site_name == 'hwroads.com' else 'HW Asphalt FL'} - Expert Services in {city_name}, Florida</title>
    <meta name="description" content="{'HW Roads provides top-quality road construction services' if site_name == 'hwroads.com' else 'HW Asphalt FL offers top-quality asphalt paving and maintenance services'} in {city_name}, FL. Trust our experienced team for all your {'road building needs' if site_name == 'hwroads.com' else 'asphalt needs'}">
    <link rel="stylesheet" href="{stylesheet}">
    <!-- Swiper CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.css" />
    {structured_data}
</head>
<body class="font-sans bg-gray-100">
    <header class="{header_class} py-4">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold">{'HW Roads - ' if site_name == 'hwroads.com' else 'HW Asphalt FL - '} {city_name} {'Road Construction' if site_name == 'hwroads.com' else 'Asphalt Experts'}</h1>
        </div>
    </header>

    <nav class="{nav_class} py-2">
        <div class="container mx-auto px-4">
            <ul class="flex space-x-4">
                <li><a href="#services" class="hover:underline">Services</a></li>
                <li><a href="#about" class="hover:underline">About Us</a></li>
                <li><a href="#contact" class="hover:underline">Contact</a></li>
            </ul>
        </div>
    </nav>

    <main class="container mx-auto px-4 py-8">
        {content}
        <section id="contact" class="bg-white p-8 rounded-lg shadow-md">
            <h2 class="text-3xl font-bold mb-6">Contact Us for Your {city_name} {'Road Project' if site_name == 'hwroads.com' else 'Asphalt Project'}</h2>
            <form action="http://localhost:5000/submit" method="POST">
                <div class="mb-4">
                    <label for="name" class="block text-gray-700 font-semibold mb-2">Name</label>
                    <input type="text" id="name" name="name" class="w-full px-3 py-2 border rounded-lg" required>
                </div>
                <div class="mb-4">
                    <label for="email" class="block text-gray-700 font-semibold mb-2">Email</label>
                    <input type="email" id="email" name="email" class="w-full px-3 py-2 border rounded-lg" required>
                </div>
                <div class="mb-4">
                    <label for="message" class="block text-gray-700 font-semibold mb-2">Message</label>
                    <textarea id="message" name="message" rows="4" class="w-full px-3 py-2 border rounded-lg" required></textarea>
                </div>
                <input type="hidden" name="site" value="{site_name}">
                <button type="submit" class="{button_class} px-6 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition duration-300">Send Message</button>
            </form>
        </section>
    </main>

    <footer class="{footer_class} py-8">
        <div class="container mx-auto px-4">
            <div class="flex flex-wrap justify-between">
                <div class="w-full md:w-1/3 mb-6 md:mb-0">
                    <h3 class="text-xl font-semibold mb-2">{'HW Roads' if site_name == 'hwroads.com' else 'HW Asphalt FL'} {city_name}</h3>
                    <p>Your trusted {'partner for road construction' if site_name == 'hwroads.com' else 'asphalt experts'} in {city_name}, Florida.</p>
                </div>
                <div class="w-full md:w-1/3 mb-6 md:mb-0">
                    <h3 class="text-xl font-semibold mb-2">Contact Us</h3>
                    <p>Phone: (555) {'123-4567' if site_name == 'hwroads.com' else '987-6543'}</p>
                    <p>Email: {'info@hwroads.com' if site_name == 'hwroads.com' else 'info@hwasphaltfl.com'}</p>
                </div>
                <div class="w-full md:w-1/3">
                    <h3 class="text-xl font-semibold mb-2">Follow Us</h3>
                    <div class="flex space-x-4">
                        <a href="#" class="hover:{'text-blue-300' if site_name == 'hwroads.com' else 'text-yellow-300'}">Facebook</a>
                        <a href="#" class="hover:{'text-blue-300' if site_name == 'hwroads.com' else 'text-yellow-300'}">Twitter</a>
                        <a href="#" class="hover:{'text-blue-300' if site_name == 'hwroads.com' else 'text-yellow-300'}">{'LinkedIn' if site_name == 'hwroads.com' else 'Instagram'}</a>
                    </div>
                </div>
            </div>
            <div class="mt-8 text-center">
                <p>&copy; 2023 {'HW Roads' if site_name == 'hwroads.com' else 'HW Asphalt FL'}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Swiper JS -->
    <script src="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.js"></script>
    <script>
        new Swiper('.swiper-container', {
            loop: true,
            pagination: {
                el: '.swiper-pagination',
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            autoplay: {
                delay: 5000,
            },
        });
    </script>
    <script src="/assets/js/scripts.js"></script>
</body>
</html>""")

def generate_site(site_name, city_name):
    site_path = site_name
    create_directory(site_path)

    # Create blog posts with research content and internal linking
    blog_path = os.path.join(site_path, 'blog')
    create_directory(blog_path)

    blog_titles = [
        "How Road Construction Projects Go from Blueprint to Reality: A Step-by-Step Guide",
        "10 Critical Factors That Determine a Successful Road Construction Project",
        "Enhancing Road Durability in South East Florida's Climate",
        "Eco-Friendly Road Construction Methods for Florida",
        "Navigating Florida's Road Construction Regulations",
        "Top 5 Road Construction Services in South East Florida"
    ]

    for i, title in enumerate(blog_titles, 1):
        filename = f'post{i}.html'
        filepath = os.path.join(blog_path, filename)
        content = generate_blog_content(title)  # This now includes internal linking
        generate_html_file(filepath, title, site_name, city_name, content)

    # Create main pages
    main_pages = ['index.html', 'about.html', 'contact.html']
    for page in main_pages:
        title = page.replace('.html', '').capitalize()
        filepath = os.path.join(site_path, page)
        generate_html_file(filepath, f"{site_name} - {title}", site_name, city_name)

    # Create services pages
    services_path = os.path.join(site_path, 'services')
    create_directory(services_path)
    for i in range(1, 21):
        filename = f'service{i}.html'
        title = f"Service {i}"
        filepath = os.path.join(services_path, filename)
        generate_html_file(filepath, f"{site_name} - {title}", site_name, city_name)

    # Create additional pages
    additional_path = os.path.join(site_path, 'pages')
    create_directory(additional_path)
    for i in range(1, 30):
        filename = f'page{i}.html'
        title = f"Page {i}"
        filepath = os.path.join(additional_path, filename)
        generate_html_file(filepath, f"{site_name} - {title}", site_name, city_name)

    # Create assets directories
    assets_css = os.path.join(site_path, 'assets', 'css')
    assets_js = os.path.join(site_path, 'assets', 'js')
    assets_images = os.path.join(site_path, 'assets', 'images')
    assets_fonts = os.path.join(site_path, 'assets', 'fonts')
    for path in [assets_css, assets_js, assets_images, assets_fonts]:
        create_directory(path)

    # Create forms directory with lead-capture.html
    forms_path = os.path.join(site_path, 'forms')
    create_directory(forms_path)
    lead_capture_path = os.path.join(forms_path, 'lead-capture.html')
    generate_html_file(lead_capture_path, "Lead Capture", site_name, city_name)

    print(f"Generated file structure for {site_name}")

class EnhancedPageGenerator:
    def __init__(self):
        self.seo_generator = SEOContentGenerator()
        self.image_optimizer = ImageOptimizer()
        self.schema_generator = SchemaGenerator()
        self.performance_monitor = PerformanceMonitor()
        self.content_checker = ContentQualityChecker()
        self.location_manager = LocationManager()
        self.review_generator = ReviewGenerator()

    def generate_enhanced_page(self, template, data):
        # Generate SEO content
        meta_description = self.seo_generator.generate_meta_description(data['content'])
        location_content = self.seo_generator.generate_location_specific_content(
            data['content'],
            data['location'],
            data['industry_terms']
        )

        # Optimize images
        optimized_images = {}
        for image in data['images']:
            optimized_images[image] = self.image_optimizer.optimize_image(
                image,
                data['output_dir']
            )

        # Generate schema
        schema = self.schema_generator.generate_service_schema(
            data['service'],
            data['location']
        )

        # Check content quality
        quality_metrics = self.content_checker.check_content(location_content)

        # Generate service areas content
        service_areas_content = self.location_manager.generate_service_area_content(
            data['location']
        )

        # Generate reviews
        reviews_content = self.review_generator.generate_review_section(
            data['company_name'],
            data['location'],
            data['service_type']
        )

        # Generate service area map
        map_path = f"assets/images/service-area-{data['location'].lower()}.html"
        self.location_manager.generate_service_area_map(
            data['location'],
            map_path
        )

        # Add new content to page
        location_specific = self.seo_generator.generate_location_specific_content(
            data['content'] + service_areas_content + reviews_content,
            data['location'],
            data['industry_terms']
        )

        # Generate page
        page_content = template.render(
            content=location_specific,
            meta_description=meta_description,
            images=optimized_images,
            schema=schema,
            **data
        )

        # Monitor performance
        metrics = self.performance_monitor.measure_page_performance(data['url'])

        return {
            'content': page_content,
            'metrics': metrics,
            'quality': quality_metrics
        }

if __name__ == "__main__":
    generate_site('hwroads.com', 'Miami')
    generate_site('hwasphaltfl.com', 'Orlando')
