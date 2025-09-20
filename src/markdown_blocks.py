# markdown_blocks.py

import re
from enum import Enum
from htmlnode import (
    HTMLNode,
)

class BlockType(Enum): 
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_block): 
    if re.match(r'#{1,6}\s+.*', markdown_block):
        return BlockType.HEADING
    elif re.match(r'`{3}.*`{3}', markdown_block, re.S):
        return BlockType.CODE
    elif re.search(r'^>.*', markdown_block, re.M):
        return BlockType.QUOTE
    elif re.search(r'-\s.*', markdown_block, re.M):
        return BlockType.UNORDERED_LIST
    elif matches_ordered_list(markdown_block): 
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def matches_ordered_list(markdown_block):
    i = 1
    for line in markdown_block.split('\n'):
        regex = f"{i}" + r'\.\s.*'
        match = re.match(regex, line)
        if not match: 
            return False
        i += 1
    return True

def markdown_to_blocks(markdown): 
    final_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks: 
        if block == "":
            continue
        stripped_block = block.strip()
        final_blocks.append(stripped_block)
    return final_blocks

def markdown_to_html_node(markdown): 
    blocks = markdown_to_blocks(markdown)
    for block in blocks: 
        block_type = block_to_block_type(block)
        HTMLNode


