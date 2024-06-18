import os
import shutil
import logging

logging.basicConfig(level=logging.INFO)

# poner el path absoluto al archivo
folder = r""

def move_files_to_main_folder(src_folder, dst_folder):
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        if os.path.isdir(src_path):
            # recursivamente mover todo al sub directorio
            move_files_to_main_folder(src_path, dst_folder)
            # remuevo el subdirectorio
            os.rmdir(src_path)
        else:
            dst_path = os.path.join(dst_folder, item)
            try:
                logging.info(f'Moving {src_path} to {dst_path}')
                shutil.move(src_path, dst_path)
            except Exception as e:
                logging.error(f'Error moving {src_path} to {dst_path}: {e}')

# Initial call to move files from all subdirectories of the main folder
subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]

for sub in subfolders:
    move_files_to_main_folder(sub, folder)
