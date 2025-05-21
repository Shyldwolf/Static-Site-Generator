import unittest
from src.htmlnode import HTMLNode

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
        
        
        
        
if __name__ == "__main__":
    unittest.main()