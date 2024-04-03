# Knowledge Crawler

- Using Playwright, go to a URL.
- Save `.html` content from the page.
- Convert the `.html` content to Markdown.
- Clean up the Markdown content using a Large Language Model (in this case, Claude 3 Haiku).
- Save the extracted knowledge to a `.md` file. (TODO: Replace this with a Knowledge Graph like Neo4j)

## Limitations
It doesn't extract information from images or videos, only text content. So it works decently well for FAQs, Wikis, and Blogs. Not so much for YouTube or Instagram.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Make sure you have an `ANTHROPIC_API_KEY` in your environment variables. You can get one from the [Anthropic Console](https://console.anthropic.com/settings/keys) which requires an account with billing setup.

```bash
# .bashrc or .bash_profile
export ANTHROPIC_API_KEY=your-api-key-here
```

### Running the Project
```bash
python app.py http://your-url.here
```

Example:
```bash
python app.py https://en.wikipedia.org/wiki/April_Fools%27_Day
```