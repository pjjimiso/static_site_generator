# test_extract_markdown.py

import unittest
from extract_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    extract_markdown_title,
)


class TestExtractMarkdown(unittest.TestCase): 
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)."
        images = extract_markdown_images(text)
        self.assertEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )


    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )


    def test_extract_markdown_links_with_quotes(self): 
        text = 'Here is a link: [I love "The Lord of the Rings"](https://en.wikipedia.org/wiki/The_Lord_of_the_Rings_(film_series))'
        link = extract_markdown_links(text)
        self.assertEqual(
            link,
            [
                ('I love "The Lord of the Rings"', "https://en.wikipedia.org/wiki/The_Lord_of_the_Rings_(film_series)")
            ]
        )


    def test_extract_markdown_combined(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg). This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)
        self.assertEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )
        self.assertEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

    def test_extract_markdown_title(self):
        md = """
# This is the title   

## Here is a header

This is paragraph text
"""
        title = extract_markdown_title(md)
        self.assertEqual(
            title,
            "This is the title"
        )

    def test_extract_markdown_no_title(self): 
        md = """
## This is a header, not a title!

something something something
"""
        with self.assertRaises(ValueError):
            title = extract_markdown_title(md)

