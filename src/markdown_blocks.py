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


def block_to_html_node(block): 
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH: 
        return paragraph_to_html_node(block)
    elif block_type == BlockType.CODE: 
        return code_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    else:
        raise ValueError("Invalid block type")


def markdown_to_html_node(markdown): 
    children= []
    blocks = markdown_to_blocks(markdown)
    for block in blocks: 
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode(tag="div", children=children)


def text_to_children(text):
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes: 
        children.append(text_node_to_html_node(textnode))
    return children


def heading_to_html_node(block):
    tag = parse_heading_number(block)
    text = re.sub("#{1,6}", "", block, re.M)
    children = text_to_children(text.strip())
    return ParentNode(tag=tag, children=children)


def parse_heading_number(block): 
    match = re.match(r'^(#{1,6})\s*(.*)', block)
    tag = f"h{len(match.group(1))}"
    return tag


def olist_to_html_node(block): 
    html_nodes = []
    for line in block.split("\n"):
        text = re.sub("\d+\.\s+", "", line, re.M)
        children = text_to_children(text)
        html_nodes.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ol", children=html_nodes)


def ulist_to_html_node(block):
    html_nodes = []
    for line in block.split("\n"):
        text = re.sub("-\s+", "", line)
        children = text_to_children(text)
        html_nodes.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=html_nodes)


def code_to_html_node(block): 
    children = []
    text = re.sub("```", "", block, re.M)
    textnode = TextNode(text.strip(), TextType.TEXT)
    children.append(text_node_to_html_node(textnode))
    code_node = [ParentNode(tag="code", children=children)]
    return ParentNode(tag="pre", children=code_node)


def quote_to_html_node(block): 
    new_lines = []
    for line in block.split("\n"):
        if not line.startswith(">"): 
            raise ValueError("Invalid quote block")
        new_line = line.lstrip(">").strip()
        if new_line == "":
            continue
        new_lines.append(new_line)
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode(tag="blockquote", children=children)


def paragraph_to_html_node(block): 
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode(tag="p", children=children)






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


