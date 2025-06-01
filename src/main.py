import sys
import shutil
import os
from src.converts import generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    dest_dir = "docs"


    print(basepath)
    print(dest_dir)

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    copy_static_to_docs()

    generate_pages_recursive("content", "template.html", dest_dir, basepath)

def copy_static_to_docs(static_dir="static", public_dir="docs"):
    os.makedirs(public_dir, exist_ok=True)
    
    for item in os.listdir(static_dir):
        s = os.path.join(static_dir, item)
        d = os.path.join(public_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
            
            
if __name__ == "__main__":
    main()
