class SchemaGenerator:
    def generate_service_schema(self, service, location):
        return {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": service['name'],
            "description": service['description'],
            "provider": {
                "@type": "LocalBusiness",
                "name": "HW Roads",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": location,
                    "addressRegion": "FL"
                }
            },
            "areaServed": {
                "@type": "City",
                "name": location
            },
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Road Construction Services",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": service_name
                        }
                    } for service_name in service['subServices']
                ]
            }
        }
