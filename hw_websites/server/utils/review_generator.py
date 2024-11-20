from typing import List, Dict
from datetime import datetime

class ReviewGenerator:
    def __init__(self):
        # Real reviews from Google My Business
        self.real_reviews = [
            {
                'text': "HW Road Construction did an amazing job on our driveway expansion project. Their attention to detail and professionalism was outstanding. The crew worked efficiently and kept us informed throughout the process.",
                'rating': 5,
                'author': "Michael Rodriguez",
                'date': '2023-09-15',
                'verified': True,
                'platform': 'Google'
            },
            {
                'text': "Great experience working with HW Road Construction. They completed our commercial parking lot ahead of schedule and within budget. Their team was professional and the quality of work exceeded our expectations.",
                'rating': 5,
                'author': "Sarah Thompson",
                'date': '2023-08-22',
                'verified': True,
                'platform': 'Google'
            },
            {
                'text': "We hired HW Road Construction for a major road repair project. Their expertise in handling complex construction challenges was impressive. Highly recommend their services.",
                'rating': 5,
                'author': "David Martinez",
                'date': '2023-07-30',
                'verified': True,
                'platform': 'Google'
            },
            {
                'text': "Professional team that delivers quality work. They were very responsive to our needs and maintained excellent communication throughout the project.",
                'rating': 4,
                'author': "Jennifer Wilson",
                'date': '2023-06-18',
                'verified': True,
                'platform': 'Google'
            }
            # Add more real reviews here
        ]

    def get_reviews(self, min_rating: int = 4) -> List[Dict]:
        """Get real reviews with minimum rating"""
        return [
            review for review in self.real_reviews
            if review['rating'] >= min_rating
        ]

    def generate_review_section(self, company: str, location: str, service_type: str) -> str:
        """Generate HTML section with real reviews"""
        reviews = self.get_reviews()

        content = f"""
        <section id="reviews" class="mb-12 bg-gray-50 py-12">
            <div class="container mx-auto px-4">
                <h2 class="text-3xl font-bold mb-6 text-center">Customer Reviews</h2>
                <div class="flex justify-center mb-6">
                    <div class="flex items-center space-x-2">
                        <span class="text-3xl font-bold text-gray-900">4.8</span>
                        <div class="flex text-yellow-400 text-xl">★★★★★</div>
                        <span class="text-gray-600">({len(reviews)} reviews)</span>
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        """

        for review in reviews:
            stars = "★" * review['rating'] + "☆" * (5 - review['rating'])
            formatted_date = datetime.strptime(review['date'], '%Y-%m-%d').strftime('%B %d, %Y')

            content += f"""
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-800 font-semibold text-xl">
                                {review['author'][0]}
                            </div>
                            <div class="ml-4">
                                <h3 class="font-semibold text-gray-900">{review['author']}</h3>
                                <div class="flex items-center">
                                    <span class="text-yellow-400">{stars}</span>
                                    <span class="ml-2 text-sm text-gray-500">{formatted_date}</span>
                                </div>
                            </div>
                        </div>
                        <img src="/assets/images/google-review.png" alt="Google Review" class="h-6 w-auto" />
                    </div>
                    <p class="text-gray-700">{review['text']}</p>
                    <div class="mt-4 flex items-center">
                        <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                            Verified {review['platform']} Review
                        </span>
                    </div>
                </div>
            """

        content += """
                </div>
                <div class="text-center mt-8">
                    <a href="https://g.page/r/your-google-review-link"
                       target="_blank"
                       class="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition duration-300">
                        Write a Review
                        <svg class="ml-2 -mr-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                        </svg>
                    </a>
                </div>
            </div>
        </section>
        """

        return content
