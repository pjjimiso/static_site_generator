# test_split_nodes.py

import unittest
from textnode import TextNode, TextType
from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image, 
    split_nodes_link,
    text_to_textnodes
)


class TestSplitNodes(unittest.TestCase): 
    def test_split_text(self):
        node = TextNode("This is just some text", TextType.TEXT)
        with self.assertRaises(ValueError): 
            new_nodes = split_nodes_delimiter([node], '', TextType.BOLD)

    def test_split_bold(self):
        node = TextNode("This is text with a **bold phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("bold phrase", TextType.BOLD, None), 
                TextNode(" in the middle", TextType.TEXT, None)
            ]
        )

    def test_split_italic(self): 
        node = TextNode("This text has _meaning!_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This text has ", TextType.TEXT, None),
                TextNode("meaning!", TextType.ITALIC, None)
            ]
        )

    def test_split_code(self): 
        node = TextNode("Let's write a `Hello, world!` program!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("Let's write a ", TextType.TEXT, None),
                TextNode("Hello, world!", TextType.CODE, None), 
                TextNode(" program!", TextType.TEXT, None),
            ]
        )

    def test_split_multiple(self): 
        node1 = TextNode("Is it `Hello World!`", TextType.TEXT) 
        node2 = TextNode("...or `Hello, world!`?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("Is it ", TextType.TEXT, None),
                TextNode("Hello World!", TextType.CODE, None), 
                TextNode("...or ", TextType.TEXT, None),
                TextNode("Hello, world!", TextType.CODE, None), 
                TextNode("?", TextType.TEXT, None), 
            ]
        )

    def test_split_link(self): 
        node = TextNode("This is text with a link [my youtube](https://www.youtube.com/@thumpertherapy)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a link ", TextType.TEXT, None),
                TextNode("my youtube", TextType.LINK, "https://www.youtube.com/@thumpertherapy"),
            ]
        )

    def test_split_no_links(self): 
        node = TextNode("There is no link in this string!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("There is no link in this string!", TextType.TEXT, None)
            ]
        )

    def test_split_links_multiple(self):
        node = TextNode("Here is a link to my youtube channel: [ThumperTherapy Youtube](https://www.youtube.com/@thumpertherapy) and my personal blog: [Pat Blog](https://www.thumpertherapy.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is a link to my youtube channel: ", TextType.TEXT, None),
                TextNode("ThumperTherapy Youtube", TextType.LINK, "https://www.youtube.com/@thumpertherapy"),
                TextNode(" and my personal blog: ", TextType.TEXT, None),
                TextNode("Pat Blog", TextType.LINK, "https://www.thumpertherapy.com"),
            ]
        )

    def test_split_links_multiple_nodes(self): 
        node1 = TextNode("This is text with a link [my youtube](https://www.youtube.com/@thumpertherapy)", TextType.TEXT)
        node2 = TextNode("This string doesn't have any links!", TextType.TEXT)
        node3 = TextNode("Here is a link to my youtube channel: [ThumperTherapy Youtube](https://www.youtube.com/@thumpertherapy) and my personal blog: [Pat Blog](https://www.thumpertherapy.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a link ", TextType.TEXT, None),
                TextNode("my youtube", TextType.LINK, "https://www.youtube.com/@thumpertherapy"),
                TextNode("This string doesn't have any links!", TextType.TEXT, None),
                TextNode("Here is a link to my youtube channel: ", TextType.TEXT, None),
                TextNode("ThumperTherapy Youtube", TextType.LINK, "https://www.youtube.com/@thumpertherapy"),
                TextNode(" and my personal blog: ", TextType.TEXT, None),
                TextNode("Pat Blog", TextType.LINK, "https://www.thumpertherapy.com"),
            ]
         )

    def test_split_image(self): 
        node = TextNode("Here's a cool image!![cute mug](https://i.imgur.com/iAjslkw.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes, 
            [
                TextNode("Here's a cool image!", TextType.TEXT, None),
                TextNode("cute mug", TextType.IMAGE, "https://i.imgur.com/iAjslkw.png"),
            ]
        )

    def test_split_no_image(self): 
        node = TextNode("This line is **JUST TEXT!**", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This line is **JUST TEXT!**", TextType.TEXT, None)
            ]
        )

    def test_split_images_multiple(self):
        node = TextNode("Here's a cool image!![cute mug](https://i.imgur.com/iAjslkw.png) and here's another:![doggo](https://i.imgur.com/doggo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here's a cool image!", TextType.TEXT, None),
                TextNode("cute mug", TextType.IMAGE, "https://i.imgur.com/iAjslkw.png"),
                TextNode(" and here's another:", TextType.TEXT, None),
                TextNode("doggo", TextType.IMAGE, "https://i.imgur.com/doggo.png"),
            ]
        )

    def test_split_images_multiple_nodes(self): 
        node1 = TextNode("Here's a cool image!![cute mug](https://i.imgur.com/iAjslkw.png)", TextType.TEXT)
        node2 = TextNode("This line is **JUST TEXT!**", TextType.TEXT)
        node3 = TextNode("Here's a cool image!![cute mug](https://i.imgur.com/iAjslkw.png) and here's another:![doggo](https://i.imgur.com/doggo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertEqual(
            new_nodes, 
            [
                TextNode("Here's a cool image!", TextType.TEXT, None),
                TextNode("cute mug", TextType.IMAGE, "https://i.imgur.com/iAjslkw.png"),
                TextNode("This line is **JUST TEXT!**", TextType.TEXT, None),
                TextNode("Here's a cool image!", TextType.TEXT, None),
                TextNode("cute mug", TextType.IMAGE, "https://i.imgur.com/iAjslkw.png"),
                TextNode(" and here's another:", TextType.TEXT, None),
                TextNode("doggo", TextType.IMAGE, "https://i.imgur.com/doggo.png"),
            ]
         )

    def test_text_to_textnodes(self): 
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_textnodes = text_to_textnodes(text)
        self.assertListEqual(
            new_textnodes,
            [
                TextNode("This is " , TextType.TEXT, None),
                TextNode("text", TextType.BOLD, None),
                TextNode(" with an ", TextType.TEXT, None),
                TextNode("italic", TextType.ITALIC, None),
                TextNode(" word and a ", TextType.TEXT, None),
                TextNode("code block", TextType.CODE, None),
                TextNode(" and an ", TextType.TEXT, None),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_empty_text_to_textnodes(self): 
        nodes = text_to_textnodes("")
        self.assertListEqual(
            nodes,
            []
        )

    def test_invalid_text_to_textnodes(self): 
        with self.assertRaises(ValueError): 
            nodes = text_to_textnodes("This is **not* valid markdown format!")

