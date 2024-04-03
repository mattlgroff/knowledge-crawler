import os
from datetime import datetime
import sys
import time
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from markdownify import markdownify as md
import anthropic

def fetch_and_clean_url_to_markdown(url, api_key):
    # Fetch and convert to Markdown
    print(f"Fetching content from {url} now...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch the browser
        page = browser.new_page()  # Open a new browser page
        page.goto(url, wait_until='networkidle')  # Navigate to the URL
        html_content = page.content()  # Get the page content
        browser.close()  # Close the browser

    print("Converting HTML to Markdown...")
    markdown_content = md(html_content)  # Convert HTML to Markdown

    # Clean the Markdown using anthropic API
    client = anthropic.Client(api_key=api_key)
    system_message = """
      # Your Purpose
      You are a distiller of knowledge from Markdown Documents extracted from crawling the Web. You bring order from chaos, and knowledge from order.

      ## Your Goal
      Your goal is to take the jumbled mess of information provided and rewrite it: removing unnecessary information, and making it more readable.
      You will remove links to other web pages, and any other information that is not directly related to the content of the page.
      You will also remove any images, and any other information that is not directly related to the content of the page.
      Your goal is a clean Markdown Document that strictly contains the content of the page without any of the extra fluff.
      For example, if I gave you a Wikipedia Markdown, you'd remove the links to other Wikipedia pages, and any other information that is not directly related to the content of the page.

      ## Your Output
      You will output a clean Markdown Document that strictly contains the content of the page without any of the extra fluff. Return only Markdown. Begin with #
    """

    start_time = time.time()

    print("Cleaning extracted Markdown with a Large Language Model (Claude 3 Haiku)...")
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        system=system_message,
        messages=[
            {"role": "user", "content": f"Here is the Markdown Document you need to cleanup from the Web: \n{markdown_content}"},
        ],
        max_tokens=4096
    )

    print(f"Response time from Claude 3 Haiku: {time.time() - start_time}\n")

    cleaned_markdown_content = response.content[0].text

  # Ensure the knowledge directory exists
    os.makedirs('./knowledge', exist_ok=True)

    # Format the current time and date for the filename
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    parsed_url = urlparse(url)
    filename = f"./knowledge/{parsed_url.netloc.replace('www.', '')}_{current_time}.md"
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(cleaned_markdown_content)
    
    print(f"Markdown saved to {filename}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)
    fetch_and_clean_url_to_markdown(url, api_key)
