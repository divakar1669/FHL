from bs4 import BeautifulSoup

def extract_text_from_html(html_content):
    """Extract and return plain text from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)