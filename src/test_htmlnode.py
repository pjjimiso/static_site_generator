# test_htmlnode.py

import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        child_node = HTMLNode(
            "a",
            "Website", 
            None, 
            {"href": "https://thumpertherapy.com", "target": "_blank",}
        )
        parent_node = HTMLNode("li", "this is a list", [child_node])
        self.assertEqual(parent_node.tag, "li")
        self.assertEqual(parent_node.value, "this is a list")
        self.assertEqual(parent_node.children, [child_node])
        self.assertEqual(parent_node.props, None)

    def test_repr(self):
        node = HTMLNode("a", "Website", None, {"href": "https://thumpertherapy.com"})
        self.assertEqual(
                node.__repr__(), 
                "HTMLNode(a, Website, children: None, {'href': 'https://thumpertherapy.com'})"
        )

    def test_props_to_html(self):
        node = HTMLNode(
            "a", 
            "Website", 
            None, 
            {"href": "https://thumpertherapy.com", "target": "_blank",}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' href="https://thumpertherapy.com" target="_blank"'
        )
