from src.funcs import copiar_static_a_public, generate_page
import os
import shutil

def main():
    
    if os.path.exists("public"):
        shutil.rmtree("public")

  
    copiar_static_a_public()

   
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()


