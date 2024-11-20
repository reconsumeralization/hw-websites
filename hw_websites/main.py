import os
from dotenv import load_dotenv
from hw_websites.server.generate_pages import EnhancedPageGenerator
from hw_websites.server.server import app

def main():
    # Load environment variables
    load_dotenv()

    # Initialize the page generator
    generator = EnhancedPageGenerator()

    # Define site data
    sites_data = {
        'hwroads.com': {
            'cities': ['Miami', 'Fort Lauderdale', 'West Palm Beach'],
            'company_name': 'HW Roads',
            'service_type': 'road construction',
            'industry_terms': [
                'road construction',
                'highway development',
                'infrastructure projects'
            ]
        },
        'hwasphaltfl.com': {
            'cities': ['Orlando', 'Tampa', 'Jacksonville'],
            'company_name': 'HW Asphalt FL',
            'service_type': 'asphalt paving',
            'industry_terms': [
                'asphalt paving',
                'parking lot construction',
                'driveway installation'
            ]
        }
    }

    # Generate sites
    for site_name, data in sites_data.items():
        for city in data['cities']:
            page_data = {
                'company_name': data['company_name'],
                'location': city,
                'service_type': data['service_type'],
                'industry_terms': data['industry_terms'],
                'images': [
                    f'assets/images/{site_name}/project1.jpg',
                    f'assets/images/{site_name}/project2.jpg',
                    f'assets/images/{site_name}/project3.jpg'
                ],
                'output_dir': f'output/{site_name}/{city.lower()}',
                'url': f'https://{site_name}',
                'content': f'Content for {data["company_name"]} in {city}',
                'service': {
                    'name': data['service_type'],
                    'description': f'Professional {data["service_type"]} services in {city}',
                    'subServices': [
                        'Residential Projects',
                        'Commercial Projects',
                        'Municipal Projects'
                    ]
                }
            }

            # Generate enhanced page
            result = generator.generate_enhanced_page(
                template=None,  # You'll need to create a Jinja2 template
                data=page_data
            )

            # Log results
            print(f"Generated {site_name} for {city}")
            print(f"Performance metrics: {result['metrics']}")
            print(f"Quality metrics: {result['quality']}")

if __name__ == "__main__":
    # Run the Flask app in a separate thread
    from threading import Thread
    server = Thread(target=app.run)
    server.start()

    # Run the main generation script
    main()
