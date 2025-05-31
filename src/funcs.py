from .textnode import TextNode, TextType
from .htmlnode import ParentNode, LeafNode
from .blocknode import BlockType, block_to_block_type
import re
import textwrap
import os
import shutil



def split_nodes_delimiter(old_nodes, delimiter, text_type): # Split nodes based on a delimiter and assign a text type to the split parts.
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

def extract_markdown_images(text): # Extract images from markdown text.
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text): # Extract links from markdown text.
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    return re.findall(pattern, text)  

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

            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

            # Crear nodo IMAGE con texto y URL juntos
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))

            last_index = end

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

            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

            # Creamos un TextNode tipo LINK con texto y url
            new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))

            last_index = end

        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes

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

def markdown_to_html_node(markdown):
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
            child_html_nodes = [textnode_to_htmlnode(tn) for tn in text_nodes]

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
                li_children = [textnode_to_htmlnode(tn) for tn in text_nodes]
                li_nodes.append(ParentNode(tag="li", children=li_children))
            ul_node = ParentNode(tag="ul", children=li_nodes)
            children.append(ul_node)

        elif block_type == BlockType.ORDERED_LIST:
            items = block.splitlines()
            li_nodes = []
            for item in items:
                content = item[item.find('.')+1:].strip()
                text_nodes = text_to_children(content)
                li_children = [textnode_to_htmlnode(tn) for tn in text_nodes]
                li_nodes.append(ParentNode(tag="li", children=li_children))
            ol_node = ParentNode(tag="ol", children=li_nodes)
            children.append(ol_node)

        elif block_type == BlockType.BLOCKQUOTE:
            lines = [line[1:].strip() for line in block.splitlines()]
            text = " ".join(lines).strip()  # Juntamos todas las líneas en un solo texto
            text_nodes = text_to_children(text)
            child_html_nodes = [textnode_to_htmlnode(tn) for tn in text_nodes]
            blockquote_node = ParentNode(tag="blockquote", children=child_html_nodes)
            children.append(blockquote_node)

        elif block_type == BlockType.CODE:
            code_text = block.strip('```').strip()
            code_node = LeafNode(tag="code", value=code_text)
            pre_node = ParentNode(tag="pre", children=[code_node])
            children.append(pre_node)

        else:
            text_nodes = text_to_children(block)
            child_html_nodes = [textnode_to_htmlnode(tn) for tn in text_nodes]
            p_node = ParentNode(tag="p", children=child_html_nodes)
            children.append(p_node)

    return ParentNode(tag="div", children=children)



def textnode_to_htmlnode(textnode):
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
        return LeafNode(tag="img", props={"src": textnode.url, "alt": textnode.text})
    else:
        print(f"[ERROR] Unknown text type: {textnode.text_type} (text: {textnode.text})")
        raise ValueError("Unknown text type")




def copiar_static_a_public(origen="static", destino="public"): # Copy the contents of the 'static' directory to the 'public' directory, removing the destination directory if it exists.
   
    if os.path.exists(destino):
        shutil.rmtree(destino)
        print(f"[INFO] Carpeta eliminada: {destino}")
    
    def copiar_recursivo(src, dst):
        os.makedirs(dst, exist_ok=True)

        for item in os.listdir(src):
            ruta_src = os.path.join(src, item)
            ruta_dst = os.path.join(dst, item)

            if os.path.isdir(ruta_src):
                copiar_recursivo(ruta_src, ruta_dst)
            else:
                shutil.copy2(ruta_src, ruta_dst)
                print(f"[COPIADO] {ruta_src} -> {ruta_dst}")
    
    copiar_recursivo(origen, destino)

def extract_title(markdown: str) -> str: # Extract the first H1 title from the markdown text.
    for line in markdown.splitlines():
        if line.strip().startswith("# "):  # H1 header
            return line.strip()[2:].strip()
    raise Exception("No H1 title found in the markdown.")

def remove_title_line(markdown: str) -> str:
    lines = markdown.splitlines()
    new_lines = [line for line in lines if not line.strip().startswith("# ")]
    return "\n".join(new_lines)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    markdown_without_title = remove_title_line(markdown)

    html_node = markdown_to_html_node(markdown_without_title)
    html = html_node.to_html()

    html_with_title = f"<h1>{title}</h1>{html}"

    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_with_title)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)