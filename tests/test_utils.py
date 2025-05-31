import unittest
import re
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import TextNode, TextType
from src.funcs import markdown_to_html_node, markdown_to_blocks, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnode
from src.blocknode import block_to_block_type, BlockType
from src.funcs import extract_title

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):# Test for HTMLNode initialization
        node = HTMLNode("div", "Hello, World!", [], {"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "greeting"})
        
        
        
    def test_props_to_html_single_prop(self): # Test for converting single prop to HTML
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\"")

    def test_props_to_html_multiple_props(self): # Test for converting multiple props to HTML
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank"
     })
    
        result = node.props_to_html() # Test for converting multiple props to HTML
        self.assertTrue(
            result == " href=\"https://www.google.com\" target=\"_blank\"" or 
            result == " target=\"_blank\" href=\"https://www.google.com\""
        )

    def test_props_to_html_no_props(self): # Test for HTMLNode with no props
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        
    def test_leafnode(self): # Test for LeafNode initialization
        node = HTMLNode("p", "HELLO WORLD", [], {"class": "greeting"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "HELLO WORLD")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "greeting"})
        
        
    def test_parentnode(self): # Test for ParentNode initialization
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
        
    def test_to_html_with_children(self): #test for ParentNode to_html with children
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self): # Test for ParentNode with grandchildren
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_textnode_to_htmlnode(self): # Test for converting TextNode to HTMLNode
    
        text_node = TextNode("Hello, World!", TextType.TEXT)
        html_node = ParentNode.textnode_to_htmlnode(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Hello, World!")
        
        text_node = TextNode("Hello, World!", TextType.BOLD)
        html_node = ParentNode.textnode_to_htmlnode(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        
    def test_text(self): # Test for converting TextNode to HTMLNode with no tag
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = ParentNode.textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_code_delimiter_split(self): # Test for splitting TextNode with code delimiters
        old_nodes = [TextNode("This is `code` and `more code` here.", TextType.TEXT)]
        
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

    # Test for markdown image extraction and link extraction
            
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)
        
    def test_split_nodes_image(self): # Test for splitting nodes with images
        old_nodes = [TextNode("This is ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        
        new_nodes = split_nodes_image(old_nodes)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("image", TextType.TEXT),
            TextNode("https://i.imgur.com/zjjcJKZ.png", TextType.IMAGE)
        ]

        self.assertEqual(new_nodes, expected)
        
    def test_split_nodes_link(self): # Test for splitting nodes with links
        old_nodes = [TextNode("This is a [link](https://www.google.com)", TextType.TEXT)]
        
        new_nodes = split_nodes_link(old_nodes)

        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.TEXT),
            TextNode("https://www.google.com", TextType.LINK)
        ]

        self.assertEqual(new_nodes, expected)
        
    def text_to_textnode(text):
        
    # Bold: **text** or __text__
        if re.fullmatch(r"\*\*(.+?)\*\*", text) or re.fullmatch(r"__(.+?)__", text):
            clean = re.sub(r"^\*\*|^\_\_|(\*\*$)|(__$)", "", text)
            return TextNode(clean, TextType.BOLD)

    # Italic: *text* or _text_
        if re.fullmatch(r"\*(.+?)\*", text) or re.fullmatch(r"_(.+?)_", text):
            clean = re.sub(r"^\*|^\_|(\*$)|(_$)", "", text)
            return TextNode(clean, TextType.ITALIC)

    # Code: `text`
        if re.fullmatch(r"`(.+?)`", text):
            clean = text[1:-1]
            return TextNode(clean, TextType.CODE)

        # Plain text
        return TextNode(text, TextType.TEXT)

    def test_markdown_to_blocks(self): # Test for converting markdown to blocks
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    class TestBlockToBlockType(unittest.TestCase): # Test for converting markdown blocks to block types
        def test_heading(self):
            self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
            self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

        def test_code_block(self):
            self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)

        def test_quote_block(self):
            self.assertEqual(block_to_block_type("> This is a quote\n> Another line"), BlockType.QUOTE)

        def test_unordered_list(self):
            self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)

        def test_ordered_list(self):
            self.assertEqual(block_to_block_type("1. First\n2. Second\n3. Third"), BlockType.ORDERED_LIST)

        def test_paragraph(self):
            self.assertEqual(block_to_block_type("This is a normal paragraph with no special formatting."), BlockType.PARAGRAPH)

        def test_mixed_list_should_be_paragraph(self):
            self.assertEqual(block_to_block_type("1. First\n- not ordered"), BlockType.PARAGRAPH)

        def test_unordered_list_with_no_space(self):
            self.assertEqual(block_to_block_type("-No space"), BlockType.PARAGRAPH)
            
            
            
class TestMarkdownToHtmlNode(unittest.TestCase): # Test for converting markdown to HTMLNode
    def test_paragraph_and_heading(self):
        markdown = "# Heading\n\nThis is a paragraph"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "p")

    def test_code_block(self):
        markdown = "```\ndef hello():\n    return 'Hello'\n```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children[0].tag, "pre")
        self.assertEqual(node.children[0].children[0].tag, "code")

    import unittest


class TestExtractTitle(unittest.TestCase): # Test for extracting title from markdown
    def test_extract_valid_title(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_strip_spaces(self):
        md = "   #    Trim this title   "
        self.assertEqual(extract_title(md), "Trim this title")

    def test_raise_exception(self):
        md = "## Subtitle only\nSome content"
        with self.assertRaises(Exception):
            extract_title(md)

            
if __name__ == "__main__":
    unittest.main()