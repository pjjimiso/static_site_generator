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

def markdown_to_blocks(markdown): 
    final_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks: 
        if block == "":
            continue
        stripped_block = block.strip()
        final_blocks.append(stripped_block)
    return final_blocks

