import os
import datetime
# Crea la carpeta "Nueva carpeta" en el directorio actual.
#os.makedirs('dir1/dir2/dir3',exist_ok=True)
date = str(datetime.datetime.now().strftime("%d_%m_%y"))
file_path = 'dir1/'
os.makedirs( file_path + date,exist_ok=True)
# Crea la carpeta "Nueva carpeta" en la ruta /home/usuario/documentos.
