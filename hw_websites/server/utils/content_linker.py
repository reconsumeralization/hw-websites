from collections import defaultdict
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

class ContentLinker:
    def __init__(self):
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')

        self.stop_words = set(stopwords.words('english'))
        self.content_index = defaultdict(list)
        self.keyword_mapping = {}

    def build_keyword_index(self, pages):
        """Build an index of keywords and their corresponding pages"""
        for page in pages:
            # Extract keywords from title and content
            keywords = self.extract_keywords(page['title'] + ' ' + page['content'])

            # Add to index
            for keyword in keywords:
                self.content_index[keyword].append({
                    'url': page['url'],
                    'title': page['title'],
                    'context': self.get_keyword_context(page['content'], keyword)
                })

    def extract_keywords(self, text):
        """Extract meaningful keywords from text"""
        # Tokenize and clean text
        tokens = word_tokenize(text.lower())

        # Remove stop words and short words
        keywords = [
            word for word in tokens
            if word not in self.stop_words
            and len(word) > 3
            and word.isalnum()
        ]

        # Add multi-word phrases
        phrases = self.extract_phrases(text)
        keywords.extend(phrases)

        return set(keywords)

    def extract_phrases(self, text):
        """Extract meaningful multi-word phrases"""
        phrases = []
        # Define industry-specific phrases
        important_phrases = [
            "road construction",
            "asphalt paving",
            "highway maintenance",
            "traffic management",
            "construction services",
            "infrastructure development",
            "road repair",
            "pavement maintenance",
            "construction project",
            "road safety",
            # Add more relevant phrases
        ]

        for phrase in important_phrases:
            if phrase.lower() in text.lower():
                phrases.append(phrase)

        return phrases

    def get_keyword_context(self, content, keyword, context_words=10):
        """Get the surrounding context for a keyword"""
        # Find keyword in content
        pattern = re.compile(f'(?i)(.{{0,{context_words}}}){keyword}(.{{0,{context_words}}})')
        match = pattern.search(content)

        if match:
            return f"{match.group(1)}{keyword}{match.group(2)}"
        return ""

    def add_internal_links(self, content, url, max_links=3):
        """Add internal links to content"""
        soup = BeautifulSoup(content, 'html.parser')
        text_nodes = soup.find_all(text=True)
        links_added = 0

        for text_node in text_nodes:
            if links_added >= max_links:
                break

            if text_node.parent.name not in ['a', 'h1', 'script', 'style']:
                # Extract keywords from current text node
                keywords = self.extract_keywords(text_node)

                for keyword in keywords:
                    # Find relevant pages for this keyword
                    relevant_pages = [
                        page for page in self.content_index[keyword]
                        if page['url'] != url  # Don't link to self
                    ]

                    if relevant_pages and links_added < max_links:
                        # Create link
                        best_match = relevant_pages[0]  # Take the first match
                        new_text = text_node.replace(
                            keyword,
                            f'<a href="{best_match["url"]}" title="{best_match["title"]}">{keyword}</a>'
                        )
                        text_node.replace_with(BeautifulSoup(new_text, 'html.parser'))
                        links_added += 1

        return str(soup)

class BlogPostProcessor:
    def __init__(self):
        self.content_linker = ContentLinker()

    def process_blog_posts(self, blog_posts):
        """Process all blog posts to add internal linking"""
        # First, build the keyword index
        self.content_linker.build_keyword_index(blog_posts)

        # Then, add internal links to each post
        processed_posts = []
        for post in blog_posts:
            processed_content = self.content_linker.add_internal_links(
                post['content'],
                post['url']
            )
            processed_posts.append({
                **post,
                'content': processed_content
            })

        return processed_posts

def generate_blog_content(title):
    """Generate blog content with internal linking"""
    blog_processor = BlogPostProcessor()

    # Example blog posts data structure
    blog_posts = [
        {
            'title': "How Road Construction Projects Go from Blueprint to Reality",
            'url': '/blog/road-construction-blueprint-reality',
            'content': """
            <article>
                <h1>How Road Construction Projects Go from Blueprint to Reality</h1>
                <p>Road construction projects require careful planning and execution...</p>
                <!-- Rest of the content -->
            </article>
            """
        },
        {
            'title': "Eco-Friendly Road Construction Methods for Florida",
            'url': '/blog/eco-friendly-road-construction',
            'content': """
            <article>
                <h1>Eco-Friendly Road Construction Methods for Florida</h1>
                <p>As environmental concerns grow, sustainable road construction...</p>
                <!-- Rest of the content -->
            </article>
            """
        },
        # Add more blog posts
    ]

    # Process blog posts to add internal linking
    processed_posts = blog_processor.process_blog_posts(blog_posts)

    # Find and return the requested blog post
    for post in processed_posts:
        if post['title'] == title:
            return post['content']

    return f"<h1>{title}</h1><p>Content coming soon...</p>"
