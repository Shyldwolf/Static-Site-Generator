import sys
import shutil
import os
from src.converts import generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    dest_dir = "docs"

    # Borra la carpeta docs si existe
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # Copiar estáticos a docs (ajusta la función para copiar a docs)
    copy_static_to_docs()

    # Genera las páginas markdown convertidas a html dentro de docs
    generate_pages_recursive("content", "template.html", dest_dir, basepath)

def copy_static_to_docs():
    # Copia la carpeta static (o assets) a docs para que esté disponible en el sitio
    static_src = "static"
    static_dst = "docs/static"
    if os.path.exists(static_src):
        shutil.copytree(static_src, static_dst)

if __name__ == "__main__":
    main()
