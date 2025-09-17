# test_htmlnode.py

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_node_no_value(self): 
        node = LeafNode(
            value=None
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html(self): 
        node = LeafNode(
            tag="p", 
            value="Hello, world!"
        )
        self.assertEqual(
            node.to_html(), 
            "<p>Hello, world!</p>"
        )
    
    def test_leaf_with_props_to_html(self): 
        node = LeafNode(
            tag="a", 
            value="Click me!", 
            props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(), 
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_parent_no_children(self): 
        node = ParentNode(
            tag="p",
            children=None
        )
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parent_no_tag(self): 
        node = ParentNode(
            tag=None,
            children=None
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_with_child_to_html(self): 
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span>child</span></div>"
        )

    def test_parent_with_grandchild_to_html(self): 
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_parent_with_multiple_children_to_html(self): 
        grandchild_node = LeafNode(
            tag="a", 
            value="grandchild",
            props={"href": "http://www.thumpertherapy.com"}
        )
        child_node1 = ParentNode(
                tag="span", 
                children=[grandchild_node],
        )
        child_node2 = LeafNode(
            tag="b", 
            value="child1"
        )
        parent_node = ParentNode(
                tag="div", 
                children=[child_node1, child_node2]
        )
        self.assertEqual(
            parent_node.to_html(), 
            '<div><span><a href="http://www.thumpertherapy.com">grandchild</a></span><b>child1</b></div>'
        )
