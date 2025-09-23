# markdown_blocks.py

import re
from enum import Enum
from htmlnode import (
    HTMLNode,
    ParentNode,
    LeafNode,
)
from split_nodes import text_to_textnodes
from textnode import text_node_to_html_node
from textnode import TextNode, TextType

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

def parse_heading(block): 
    match = re.match(r'^(#{1,6})\s*(.*)', block)
    tag = f"h{len(match.group(1))}"
    return tag

def text_to_children(block, block_type=None): 
    children = []
    text = " ".join(block.split("\n"))
    if block_type == BlockType.CODE: 
        # we preserve special characters in code blocks by not running text_to_textnodes
        text = re.sub("```\s*", "", block, re.M)
        textnode = TextNode(text, TextType.TEXT)
        children.append(text_node_to_html_node(textnode))
    elif block_type == BlockType.HEADING:
        #text = block.replace("#", "")
        text = re.sub("#{1,6}\s+", "", block, re.M)
        textnodes = text_to_textnodes(text)
        for textnode in textnodes:
            children.append(text_node_to_html_node(textnode))
    elif block_type == BlockType.QUOTE: 
        text = re.sub(">\s+", "", text, re.M)
        textnodes = text_to_textnodes(text)
        for textnode in textnodes:
            children.append(text_node_to_html_node(textnode))
    elif block_type == BlockType.UNORDERED_LIST:
        for line in block.split("\n"):
            text = re.sub("-\s+", "", line, re.M)
            children.append(LeafNode(tag="li", value=text))
    elif block_type == BlockType.ORDERED_LIST:
        for line in block.split("\n"):
            text = re.sub("\d+\.\s+", "", line, re.M)
            children.append(LeafNode(tag="li", value=text))
    else:
        textnodes = text_to_textnodes(text)
        for textnode in textnodes:
            children.append(text_node_to_html_node(textnode))
    return children


def markdown_to_html_node(markdown): 
    parent_node = ParentNode(tag="div", children=[])
    blocks = markdown_to_blocks(markdown)
    for block in blocks: 
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING: 
            tag = parse_heading(block)
            children = text_to_children(block, block_type)
            parent_node.children.append(ParentNode(tag=tag, children=children))
        elif block_type == BlockType.PARAGRAPH: 
            children = text_to_children(block, block_type)
            parent_node.children.append(ParentNode(tag="p", children=children))
        elif block_type == BlockType.CODE:
            children = text_to_children(block, block_type)
            code_node = [ParentNode(tag="code", children=children)]
            parent_node.children.append(ParentNode(tag="pre", children=code_node))
        elif block_type == BlockType.QUOTE: 
            children = text_to_children(block, block_type)
            p_node = [ParentNode(tag="p", children=children)]
            parent_node.children.append(ParentNode(tag="blockquote", children=p_node))
        elif block_type == BlockType.UNORDERED_LIST: 
            children = text_to_children(block, block_type)
            parent_node.children.append(ParentNode(tag="ul", children=children))
        elif block_type == BlockType.ORDERED_LIST:
            children = text_to_children(block, block_type)
            parent_node.children.append(ParentNode(tag="ol", children=children))
    return parent_node



markdown = """
# This is a header

Here is some paragraph stuff
with **bold text**!

This is another paragraph with _italic_ text and `code` here

Here is a third paragraph

## This is another header

```
This is a **code** block and 
the formatting should _not_ change!
```

### Famous Quotes

> To be or not to be

> I think
>
> Therefore I am

## Things I enjoy (in no particular order)

- Riding motorcycles
- Hiking
- Video games

1. First item
2. Second item
3. Third item
"""
#html_node = markdown_to_html_node(markdown)
#print(f"node_to_html: {html_node.to_html()}")
#print(f"html_nodes: {html_node}")


