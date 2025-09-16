# test_htmlnode.py

import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_eq(self):
        node = HTMLNode("p", "some text inside a paragraph")
        node2 = HTMLNode("p", "some text inside a paragraph")
        self.assertEqual(node, node2)

    def test_htmlnode_neq(self):
        node = HTMLNode("p", "some text inside a paragraph", None, None)
        node2 = HTMLNode("p", "different text inside a paragraph", None, None)
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        props = {"href": "https://thumpertherapy.com", "target": "_blank",}
        node = HTMLNode("a", "Website", None, props)
        test_string = ' href="https://thumpertherapy.com" target="_blank"'
        html = node.props_to_html()
        self.assertEqual(html, test_string)

    def test_children_eq(self): 
        props = {"href": "https://thumpertherapy.com", "target": "_blank",}
        child_node = HTMLNode("a", "Website", None, props)
        children = [child_node]
        parent_node = HTMLNode("li", None, children, None)
        self.assertEqual(child_node, parent_node.children[0])
