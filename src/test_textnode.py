# test_textnode.py

import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_bold_text_eq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self): 
        node = TextNode("This is a link", TextType.LINK, "http://some-link.com")
        node2 = TextNode("This is a link", TextType.LINK, "http://some-link.com")
        self.assertEqual(node, node2)

    def test_no_url_eq(self): 
        node = TextNode("This is a plain text node", TextType.TEXT, url=None)
        node2 = TextNode("This is a plain text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_text_neq(self): 
        node = TextNode("This is a plain text node", TextType.TEXT)
        node2 = TextNode("This is a bold text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_text_type_neq(self): 
        node = TextNode("This is a plain text node", TextType.TEXT)
        node2 = TextNode("This is a plain text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase): 
    def test_text(self): 
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self): 
        bold_text_node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(bold_text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_italic(self): 
        italic_text_node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(italic_text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    
    def test_italic(self): 
        code_text_node = TextNode("This is some code text", TextType.CODE)
        html_node = text_node_to_html_node(code_text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is some code text")

    def test_link(self):
        text_node_link = TextNode("This is anchor text", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(text_node_link)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is anchor text")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self): 
        text_node_image = TextNode("", TextType.IMAGE, "/path/to/image")
        html_node = text_node_to_html_node(text_node_image)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "/path/to/image", "alt": ""})

    def test_invalid_text_type(self): 
        text_node_invalid = TextNode("Invalid TextType", "CURSIVE")
        with self.assertRaises(ValueError): 
            html_node = text_node_to_html_node(text_node_invalid)


if __name__ == "__main__":
    unittest.main()
