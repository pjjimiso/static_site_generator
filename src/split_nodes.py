# split_nodes.py


from textnode import TextNode, TextType
from extract_markdown import (
    extract_markdown_images, 
    extract_markdown_links
)


def split_nodes_delimiter(old_nodes, delimiter, text_type): 
    if delimiter == '': 
        raise ValueError("Delimiter cannot be an empty separator")
    new_nodes = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        # If there are an even number of words after the split, then there were either too many or too few delimiters 
        if len(split_nodes) % 2 == 0: 
            raise ValueError("Markdown syntax error, formatted section not closed")
        for i in range(0, len(split_nodes)): 
            if split_nodes[i] != "":
                # Even indexes will be regular TEXT strings found on either side of the delimited string
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
                # Odd indexes will be strings found inside of the delimiters
                else: 
                    new_nodes.append(TextNode(split_nodes[i], text_type))
    return new_nodes

def split_nodes_link(old_nodes): 
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue
        node_text = node.text
        links = extract_markdown_links(node_text)
        if len(links) == 0: 
            new_nodes.append(node)
            continue
        for i in range(0, len(links)): 
            anchor_text, url = links[i]
            sections = node_text.split(f"[{anchor_text}]({url})", 1)
            if len(sections) != 2: 
                raise ValueError("Markdown syntax error, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            node_text = sections[1]
            # If its the final link, add the second part of the string after the split
            if i == (len(links) - 1) and sections[1] != "": 
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes): 
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue
        node_text = node.text
        links = extract_markdown_images(node_text)
        if len(links) == 0: 
            new_nodes.append(node)
            continue
        for i in range(0, len(links)): 
            alt_text, url = links[i]
            sections = node_text.split(f"![{alt_text}]({url})", 1)
            if len(sections) != 2: 
                raise ValueError("Markdown syntax error, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            node_text = sections[1]
            # If its the final link, add the second part of the string after the split
            if i == (len(links) - 1) and sections[1] != "": 
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes


text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
text_to_textnodes(text)
