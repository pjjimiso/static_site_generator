# test_markdown_blocks.py

import unittest
from markdown_blocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node
)


class TestMarkdownBlocks(unittest.TestCase): 
    def test_markdown_to_blocks(self): 
        document = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(document)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph", 
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", 
                "- This is a list\n- with items",
            ]
        )

    def test_markdown_to_blocks_newlines(self):
        document = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(document)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )
    
    def test_block_to_block_type_code(self): 
        block = "```This is a code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )
    
    def test_multiline_code_block_to_block_type_code(self): 
        block = "```This is has some code\non multiple lines```"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )

    def test_improper_format_block_to_block_type_paragraph(self):
        block_types = set()
        valid = set()
        valid.add(BlockType.PARAGRAPH)
        blocks = [
            "#This isn't a header",
            "```This isn't a code block``",
        ]
        for block in blocks: 
            block_types.add(block_to_block_type(block))
        self.assertSetEqual(
            block_types,
            valid
        )

    def test_all_block_to_block_types(self): 
        markdown = """
# Main Heading

Regular paragraph stuff goes here

## Popular Quotes

> We suffer more in imagination than in reality - Seneca
> There is no spoon - Neo

## Code Examples

```print("Hello, world!")
Hello, world!```

## To-Do: 

1. Take out the trash
2. Clean the hot tub
3. Read a book

### Done: 

In no particular order: 

- Functional programming 
- Refactor clean_tmp script
- Go to the gym
"""
        blocks = markdown_to_blocks(markdown)
        block_types = []
        for block in blocks: 
            block_types.append(block_to_block_type(block))
        self.assertListEqual(
            block_types,
            [
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.QUOTE,
                BlockType.HEADING,
                BlockType.CODE,
                BlockType.HEADING,
                BlockType.ORDERED_LIST,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST
            ]
        )

    def test_paragraph_block_to_html_node(self):
        markdown = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_code_block_to_html_node(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_quote_block_to_html_node(self):
        md = """
> To be, or not to be:
>
> That is the question
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div><blockquote>To be, or not to be: That is the question</blockquote></div>"
        )

    def test_heading_block_to_html_node(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        )

    def test_heading_7_block_to_html_node(self):
        md = "####### There's No Such Thing As Heading 7"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>####### There's No Such Thing As Heading 7</p></div>"
        )

    def test_unordered_list_block_to_html_node(self):
        md = """
- Here is a list item
- Here is another list item
- And another
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div><ul><li>Here is a list item</li><li>Here is another list item</li><li>And another</li></ul></div>"
        )

    def test_inline_markdown_inside_unordered_list_block(self): 
        md = """
- Here is a list item
- Here is a **bold** item
- Here is an _italic_ item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Here is a list item</li><li>Here is a <b>bold</b> item</li><li>Here is an <i>italic</i> item</li></ul></div>"
        )

    def test_ordered_list_block_to_html_node(self):
        md = """
1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )


