from transformers import pipeline
import yake
import spacy

class SEOContentGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.summarizer = pipeline("summarization")
        self.kw_extractor = yake.KeywordExtractor()

    def generate_meta_description(self, content, max_length=160):
        """Generate SEO-optimized meta description"""
        summary = self.summarizer(content, max_length=max_length)[0]['summary_text']
        return summary

    def generate_location_specific_content(self, base_content, location, industry_terms):
        """Generate location-specific variations of content"""
        doc = self.nlp(base_content)

        # Replace generic terms with location-specific ones
        location_specific = base_content
        for term in industry_terms:
            location_specific = location_specific.replace(
                term,
                f"{location} {term}"
            )

        return location_specific

    def generate_faq_section(self, content):
        """Generate FAQ section based on content"""
        questions = [
            "What services do you offer in {city_name}?",
            "How long does a typical project take?",
            "What are your service areas?",
            "Do you offer free estimates?",
            "What sets you apart from other contractors?"
        ]

        # Generate answers using content analysis
        faqs = []
        for question in questions:
            answer = self._generate_answer(question, content)
            faqs.append({"question": question, "answer": answer})

        return faqs
