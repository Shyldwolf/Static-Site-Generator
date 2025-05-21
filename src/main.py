from textnode import TextNode, TextType

def main():
    # Ejemplo de uso de la clase TextNode
    text_node1 = TextNode("Hello, World!", TextType.LINK, "https://example.com")
    

    print(text_node1)  

if __name__ == "__main__":
    main()