import os
import re
import textwrap
from src.splits import split_nodes_image, split_nodes_link, split_nodes_delimiter
from src.nodes import ParentNode, LeafNode, TextNode, TextType
from src.blocknode import BlockType, block_to_block_type

def text_to_textnode(text, text_type=TextType.TEXT): # Convert a plain text string to a TextNode with a specified text type.
    
    return TextNode(text, text_type) if text else None


def markdown_to_blocks(markdown): # Convert markdown text to blocks, where each block is a paragraph, heading, code block, quote, or list.
    blocks = re.split(r'\n\s*\n', markdown.strip())
    return [textwrap.dedent(block).strip() for block in blocks if block.strip()]


def text_to_children(text):
    nodes = [TextNode(text, TextType.TEXT)]

   
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

def markdown_to_html_node(markdown, basepath="/"):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block = block.strip()
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            lines = block.splitlines()
            first_line = lines[0]
            level = len(first_line) - len(first_line.lstrip('#'))
            text = first_line[level:].strip()
            text_nodes = text_to_children(text)
            child_html_nodes = [textnode_to_htmlnode(tn, basepath) for tn in text_nodes]

            if len(child_html_nodes) == 1 and isinstance(child_html_nodes[0], LeafNode):
                node = LeafNode(tag=f"h{level}", value=child_html_nodes[0].value, props=child_html_nodes[0].props)
            else:
                node = ParentNode(tag=f"h{level}", children=child_html_nodes)
            children.append(node)

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.splitlines()
            li_nodes = []
            for item in items:
                text = item[2:].strip()
                text_nodes = text_to_children(text)
                li_children = [textnode_to_htmlnode(tn, basepath) for tn in text_nodes]
                li_nodes.append(ParentNode(tag="li", children=li_children))
            ul_node = ParentNode(tag="ul", children=li_nodes)
            children.append(ul_node)

        elif block_type == BlockType.ORDERED_LIST:
            items = block.splitlines()
            li_nodes = []
            for item in items:
                content = item[item.find('.')+1:].strip()
                text_nodes = text_to_children(content)
                li_children = [textnode_to_htmlnode(tn, basepath) for tn in text_nodes]
                li_nodes.append(ParentNode(tag="li", children=li_children))
            ol_node = ParentNode(tag="ol", children=li_nodes)
            children.append(ol_node)

        elif block_type == BlockType.BLOCKQUOTE:
            lines = [line[1:].strip() for line in block.splitlines()]
            text = " ".join(lines).strip()
            text_nodes = text_to_children(text)
            child_html_nodes = [textnode_to_htmlnode(tn, basepath) for tn in text_nodes]
            blockquote_node = ParentNode(tag="blockquote", children=child_html_nodes)
            children.append(blockquote_node)

        elif block_type == BlockType.CODE:
            code_text = block.strip('```').strip()
            code_node = LeafNode(tag="code", value=code_text)
            pre_node = ParentNode(tag="pre", children=[code_node])
            children.append(pre_node)

        else:
            text_nodes = text_to_children(block)
            child_html_nodes = [textnode_to_htmlnode(tn, basepath) for tn in text_nodes]
            p_node = ParentNode(tag="p", children=child_html_nodes)
            children.append(p_node)

    return ParentNode(tag="div", children=children)



def textnode_to_htmlnode(textnode, basepath="/"):
    if textnode.text_type == TextType.TEXT:
        return LeafNode(value=textnode.text)
    elif textnode.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=textnode.text)
    elif textnode.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=textnode.text)
    elif textnode.text_type == TextType.CODE:
        return LeafNode(tag="code", value=textnode.text)
    elif textnode.text_type == TextType.LINK:
        return LeafNode(tag="a", value=textnode.text, props={"href": textnode.url})
    elif textnode.text_type == TextType.IMAGE:
        return LeafNode(tag="img", props={
            "src": basepath + textnode.url.lstrip("/"),
            "alt": textnode.text
        })
    else:
        raise ValueError(f"Unknown text type: {textnode.text_type}")


def extract_title(markdown: str) -> str: # Extract the first H1 title from the markdown text.
    for line in markdown.splitlines():
        if line.strip().startswith("# "):  # H1 header
            return line.strip()[2:].strip()
    raise Exception("No H1 title found in the markdown.")

def remove_title_line(markdown: str) -> str:
    lines = markdown.splitlines()
    new_lines = [line for line in lines if not line.strip().startswith("# ")]
    return "\n".join(new_lines)


def generate_page(from_path, template_path, dest_path, basepath="/"):
    if not basepath.endswith('/'):
        basepath += '/'

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    content_html = markdown_to_html_node(markdown, basepath).to_html()

    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title)\
                   .replace("{{ Content }}", content_html)\
                   .replace("{{ BasePath }}", basepath)
                   
              
              

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html)


        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for content in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, content)
        rel_path = os.path.relpath(content_path, start="content")
        dest_path = os.path.join(dest_dir_path, rel_path)

        if os.path.isdir(content_path):
            generate_pages_recursive(content_path, template_path, dest_dir_path, basepath)
        elif content.endswith(".md"):
            dest_path = dest_path.replace(".md", ".html")
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            generate_page(content_path, template_path, dest_path, basepath)



            
            