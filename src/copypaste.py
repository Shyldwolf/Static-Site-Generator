import os
import shutil



def copy_static_a_public(origen="static", destino="public"): # Copy the contents of the 'static' directory to the 'public' directory, removing the destination directory if it exists.
   
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