import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
