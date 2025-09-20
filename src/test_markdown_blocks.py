# test_markdown_blocks.py

import unittest
from markdown_blocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type
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

