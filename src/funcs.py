from .textnode import TextNode, TextType
from .htmlnode import ParentNode, HTMLNode
from .blocknode import BlockType, block_to_block_type
import re
import textwrap

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("Unmatched delimiters in text: " + node.text)

        for i in range(len(parts)):
            text = parts[i]
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes

def extract_markdown_images(text):
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    return re.findall(pattern, text)  # ← Esto de

def split_nodes_image(old_nodes):
    new_nodes = []
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = list(re.finditer(pattern, text))

        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0
        for match in matches:
            start, end = match.span()
            alt_text, url = match.groups()

            # Add text before the image markdown
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.TEXT))
            new_nodes.append(TextNode(url, TextType.IMAGE))

            last_index = end

        # Add any remaining text after the last match
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes
    
    
def split_nodes_link(old_nodes):
    new_nodes = []
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = list(re.finditer(pattern, text))

        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0
        for match in matches:
            start, end = match.span()
            link_text, link_url = match.groups()

            # Add text before the link
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

            # Add the link node
            new_nodes.append(TextNode(link_text, TextType.TEXT))
            new_nodes.append(TextNode(link_url, TextType.LINK))

            last_index = end

        # Add any remaining text after the last match
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes

def text_to_textnode(text, text_type=TextType.TEXT):
    
    return TextNode(text, text_type) if text else None



def markdown_to_blocks(markdown):
    blocks = re.split(r'\n\s*\n', markdown.strip())
    return [textwrap.dedent(block).strip() for block in blocks if block.strip()]


def text_to_children(text):
    
    # Start with a single TextNode
    nodes = [TextNode(text, TextType.TEXT)]
    # Split for code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    # Split for bold
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # Split for italic
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    # Split for images
    nodes = split_nodes_image(nodes)
    # Split for links
    nodes = split_nodes_link(nodes)
    # Remove empty nodes
    return [node for node in nodes if node.text]

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            children.append(HTMLNode("p", children=text_to_children(block)))

        elif block_type == BlockType.HEADING:
            level = len(re.match(r"(#+)", block).group(1))
            text = block[level + 1:]  # Skip `#` and space
            children.append(HTMLNode(f"h{level}", children=text_to_children(text)))

        elif block_type == BlockType.CODE:
            code_text = "\n".join(block.splitlines()[1:-1])  # Remove ``` lines
            code_node = HTMLNode("code", children=[ParentNode.textnode_to_htmlnode(TextNode(code_text, TextType.TEXT))])
            children.append(HTMLNode("pre", children=[code_node]))

        elif block_type == BlockType.QUOTE:
            quote_text = "\n".join([line[1:].lstrip() for line in block.splitlines()])
            children.append(HTMLNode("blockquote", children=text_to_children(quote_text)))

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.splitlines()
            li_nodes = [HTMLNode("li", children=text_to_children(item[2:])) for item in items]
            children.append(HTMLNode("ul", children=li_nodes))

        elif block_type == BlockType.ORDERED_LIST:
            items = block.splitlines()
            li_nodes = [HTMLNode("li", children=text_to_children(item[item.find('.') + 2:])) for item in items]
            children.append(HTMLNode("ol", children=li_nodes))

    return HTMLNode("div", children=children)
