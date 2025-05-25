#!/usr/bin/python3
import os, shutil, hashlib
from glob import glob

def files_are_equal_by_hash(file1, file2):
    # Сравнивает два файла по их hash (SHA256). Возвращает True, если файлы идентичны.
    hash1 = hashlib.sha256()
    hash2 = hashlib.sha256()
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        while chunk := f1.read(8192): hash1.update(chunk)
        while chunk := f2.read(8192): hash2.update(chunk)
    return hash1.digest() == hash2.digest()

CurentDir = os.getcwd()
EditorDir = CurentDir + "/Edit"
WorkDir = CurentDir + "/Client"
SaveDir = CurentDir + "/Update/new"

mask = ['elements.data', 'tasks.data', 'gshop?.data']

# Рекурсивно обходим все файлы в EditorDir по маскам
for pattern in mask:
    editor_files = glob(os.path.join(EditorDir, '**', pattern), recursive=True)
    for editor_file in editor_files:
        filename = os.path.basename(editor_file)
        # Ищем файл с таким же именем в WorkDir (в любом подкаталоге)
        found = False
        for root, _, files in os.walk(WorkDir):
            if filename in files:
                work_file = os.path.join(root, filename)
                found = True
                break
        save_file = os.path.join(SaveDir, filename)
        # Копируем, если файл не найден или отличается по хешу
        if not found or not files_are_equal_by_hash(editor_file, work_file):
            shutil.copy2(editor_file, save_file)
            print(f"Copied {filename} to {SaveDir}")