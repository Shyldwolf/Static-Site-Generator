from src.copypaste import copy_static_a_public
from src.converts import generate_pages_recursive
import os
import shutil

def main():
    
    if os.path.exists("public"):
        shutil.rmtree("public")

    
    copy_static_a_public()

   
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
