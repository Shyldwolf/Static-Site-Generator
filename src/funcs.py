from .textnode import TextNode, TextType
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
