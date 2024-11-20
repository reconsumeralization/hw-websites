from typing import List, Dict
import geocoder
import folium
from geopy.distance import geodesic

class LocationManager:
    def __init__(self):
        self.service_radius = 50  # miles
        self.florida_cities = self._load_florida_cities()

    def _load_florida_cities(self) -> Dict[str, tuple]:
        """Load major Florida cities and their coordinates"""
        return {
            'Miami': (25.7617, -80.1918),
            'Fort Lauderdale': (26.1224, -80.1373),
            'West Palm Beach': (26.7153, -80.0534),
            'Boca Raton': (26.3683, -80.1289),
            'Pompano Beach': (26.2379, -80.1248),
            'Hollywood': (26.0112, -80.1495),
            'Coral Springs': (26.2707, -80.2706),
            'Deerfield Beach': (26.3184, -80.0998),
            # Add more cities as needed
        }

    def generate_service_areas(self, base_city: str) -> List[str]:
        """Generate list of cities within service radius"""
        if base_city not in self.florida_cities:
            return []

        base_coords = self.florida_cities[base_city]
        service_areas = []

        for city, coords in self.florida_cities.items():
            if city != base_city:
                distance = geodesic(base_coords, coords).miles
                if distance <= self.service_radius:
                    service_areas.append({
                        'name': city,
                        'distance': round(distance, 1)
                    })

        return sorted(service_areas, key=lambda x: x['distance'])

    def generate_service_area_map(self, base_city: str, output_path: str):
        """Generate interactive service area map"""
        if base_city not in self.florida_cities:
            return

        base_coords = self.florida_cities[base_city]
        m = folium.Map(location=base_coords, zoom_start=10)

        # Add marker for base city
        folium.Marker(
            base_coords,
            popup=f"<b>{base_city}</b><br>Main Office",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

        # Add service area circle
        folium.Circle(
            base_coords,
            radius=self.service_radius * 1609.34,  # Convert miles to meters
            color='blue',
            fill=True,
            popup='Service Area'
        ).add_to(m)

        # Add markers for service areas
        service_areas = self.generate_service_areas(base_city)
        for area in service_areas:
            city = area['name']
            coords = self.florida_cities[city]
            folium.Marker(
                coords,
                popup=f"<b>{city}</b><br>{area['distance']} miles from {base_city}",
                icon=folium.Icon(color='green')
            ).add_to(m)

        m.save(output_path)

    def generate_service_area_content(self, base_city: str) -> str:
        """Generate HTML content for service areas"""
        service_areas = self.generate_service_areas(base_city)

        content = f"""
        <section id="service-areas" class="mb-12">
            <h2 class="text-3xl font-bold mb-6">Our Service Areas</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        """

        for area in service_areas:
            content += f"""
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <h3 class="text-xl font-semibold mb-2">{area['name']}</h3>
                    <p class="text-gray-600">{area['distance']} miles from {base_city}</p>
                    <a href="/services/{area['name'].lower().replace(' ', '-')}"
                       class="text-blue-600 hover:underline">View Services in {area['name']}</a>
                </div>
            """

        content += """
            </div>
            <div id="service-area-map" class="mt-8 h-96 rounded-lg overflow-hidden shadow-lg">
                <!-- Map will be loaded here -->
            </div>
        </section>
        """

        return content
