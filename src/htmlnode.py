from .textnode import TextType, TextNode



class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def to_html(self):
        raise NotImplementedError("to_html() aún no está implementado")

    
    def props_to_html(self):
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
        
        
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        
        if not self.children:
            raise ValueError("All parent nodes must have children")
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
        
   #convert textnode to htmlnode
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
            return LeafNode(tag="img", props={"src": textnode.url})
        else:
            raise ValueError("Unknown text type")
    
    
    