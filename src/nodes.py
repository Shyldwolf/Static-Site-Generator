from enum import Enum



class TextType(Enum): # Enum to represent different types of text nodes.
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode(): # Represents a text node in the document, which can be plain text, bold, italic, code, link, or image.
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return (
            isinstance(other, TextNode) and
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
      
            
class HTMLNode: # Base class for HTML nodes, which can be either leaf or parent nodes.
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def to_html(self):
        raise NotImplementedError("Subclasses must implement the to_html method")

    
    def props_to_html(self):
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
        
        
class LeafNode(HTMLNode): # Represents a leaf node in the HTML structure, which has a tag and a value.
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self):
        void_tags = {"img", "br", "hr", "input", "meta", "link"}
        if self.tag in void_tags:
            return f"<{self.tag}{self.props_to_html()} />"
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode): # Represents a parent node in the HTML structure, which can have children and a tag.
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise TypeError("All children must be instances of HTMLNode")
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"


    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
        
        
    
   
    
    
    