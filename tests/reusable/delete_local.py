import os
import shutil


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def delete_files(file_paths):
    for p in file_paths:
        delete_file(p)


def delete_folder(folder_path):
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
