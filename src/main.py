from src.copypaste import copy_static_a_public
from src.converts import generate_pages_recursive
import sys
import os
import shutil

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    output_dir = "docs"
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    
    copy_static_a_public(output_dir)
    generate_pages_recursive("content", "template.html", output_dir, basepath)

if __name__ == "__main__":
    main()
