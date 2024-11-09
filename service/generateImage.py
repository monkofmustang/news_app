import os
from dotenv import load_dotenv

load_dotenv()


def truncate_content(content: str, word_limit: int = 6) -> str:
    words = content.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '-Nepali'
    return content


def generate_image_url_from_text(text):
    prompt = truncate_content(text).replace(" ", "-")
    url = os.getenv("POLLINATION") + prompt
    return url
