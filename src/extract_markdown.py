# extract_markdown.py

import re

def extract_markdown_images(text): 
    # Match image pattern: ![alt text](url)
    matches = re.findall(r'(?<=!)\[([\w\d\s]*)]\((\S*)\)', text)
    return matches


def extract_markdown_links(text):
    # Match regular link pattern: [anchor text](url)
    matches = re.findall(r'(?<!!)\[([^\[\]]*)\]\((\S*)\)', text)
    return matches


def extract_markdown_title(markdown): 
    title = ""
    lines = markdown.strip().split("\n")
    match = re.match(r'^#{1}\s+(.*)', lines[0])
    if match: 
        title = match.group(1).strip()
    if not title: 
        raise ValueError("Invalid markdown syntax: missing title")
    return title.strip()

