import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import TextNode, TextType
from src.delimitir import split_nodes_delimiter


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):
        node = HTMLNode("div", "Hello, World!", [], {"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "greeting"})
        
        
        
    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\"")

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank"
     })
    
        result = node.props_to_html()
        self.assertTrue(
            result == " href=\"https://www.google.com\" target=\"_blank\"" or 
            result == " target=\"_blank\" href=\"https://www.google.com\""
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        
    def test_leafnode(self):
        node = HTMLNode("p", "HELLO WORLD", [], {"class": "greeting"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "HELLO WORLD")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "greeting"})
        
        
    def test_parentnode(self):
        child1 = HTMLNode("p", "Child 1")
        child2 = HTMLNode("p", "Child 2")
        parent = HTMLNode("div", None, [child1, child2], {"class": "parent"})
        
        self.assertEqual(parent.tag, "div")
        self.assertIsNone(parent.value)
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.props, {"class": "parent"})
        
        # Check if the children are correctly assigned
        self.assertEqual(parent.children[0].tag, "p")
        self.assertEqual(parent.children[1].tag, "p")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_textnode_to_htmlnode(self):
    
        text_node = TextNode("Hello, World!", TextType.TEXT)
        html_node = ParentNode.textnode_to_htmlnode(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Hello, World!")
        
        text_node = TextNode("Hello, World!", TextType.BOLD)
        html_node = ParentNode.textnode_to_htmlnode(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = ParentNode.textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_code_delimiter_split(self):
        old_nodes = [
            TextNode("This is `code` and `more code` here.", TextType.TEXT)
        ]
        delimiter = "`"
        text_type = TextType.CODE

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" here.", TextType.TEXT)
        ]

        self.assertEqual(new_nodes, expected)

        
        
        
        
if __name__ == "__main__":
    unittest.main()