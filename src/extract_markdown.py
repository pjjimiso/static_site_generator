# extract_markdown.py

import re

def extract_markdown_images(text): 
    # Match image pattern: ![alt text](url)
    matches = re.findall(r'(?<=!)\[([\w\d\s]*)]\((\S*)\)', text)
    return matches

def extract_markdown_links(text):
    # Match regular link pattern: [anchor text](url)
    matches = re.findall(r'(?<!!)\[([\w\d\s]*)]\((\S*)\)', text)
    return matches

