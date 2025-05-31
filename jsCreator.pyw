#!/usr/bin/python3
import os, shutil, hashlib, tkinter
from glob import glob

class application:
    """
    Класс приложения, который создает графический интерфейс для запуска функции btn_cliked.
    """
    def __init__(self, master=None):
        self.master = master
        self.master.title("JS Creator")
        self.master.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        # Создаем кнопку и связываем ее с функцией btn_cliked
        self.btn = tkinter.Button(self.master, text="Сканировать", command=self.btn_cliked)
        self.btn.pack(pady=20)

        self.panel = tkinter.Frame(self.master)
        self.panel.pack(expand=True, fill=tkinter.BOTH) 

        self.list = tkinter.Listbox(self.panel)
        self.list.pack(expand=True, fill=tkinter.BOTH)

    def btn_cliked(self):
        """
        Функция для обработки нажатия кнопки.
        Выполняет копирование файлов из Edit в Update/new.
        """
        mask = ['elements.data', 'tasks.data', 'gshop*.data']
        for pattern in mask:
            editor_files = glob(os.path.join(EditorDir, '**', pattern), recursive=True)
            for editor_file in editor_files:
                filename = os.path.basename(editor_file)
                work_file = None
                for root, _, files in os.walk(WorkDir):
                    if filename in files:
                        work_file = os.path.join(root, filename)
                        break
                save_file = os.path.join(SaveDir, filename)
                # Копируем, если файл не найден или отличается по содержимому
                if not work_file or not files_are_equal_by_hash(editor_file, work_file):
                    if copy_if_different(editor_file, save_file):
                        self.list.insert(tkinter.END, f"Копирование {save_file} успешно скопирован.")  
                else:
                    self.list.insert(tkinter.END, f"Файлы {editor_file}")
                    self.list.insert(tkinter.END, f"и {save_file} равны.")
                
            self.master.update_idletasks()

        self.list.insert(tkinter.END, "Сканирование завершено.")   

def files_are_equal_by_hash(file1, file2):
    # Сравнивает два файла по их hash (SHA256). Возвращает True, если файлы идентичны.
    hash1 = hashlib.sha256()
    hash2 = hashlib.sha256()
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        while chunk := f1.read(8192): hash1.update(chunk)
        while chunk := f2.read(8192): hash2.update(chunk)
    return hash1.digest() == hash2.digest()

def copy_if_different(src, dst):
    """
    Копирует файл src в dst, если dst не существует или отличается по содержимому.
    Если файлы равны — ничего не делает.
    """
    if os.path.exists(dst):
        if files_are_equal_by_hash(src, dst):
            # Файлы идентичны, пропускаем копирование
            return False
    shutil.copy2(src, dst)
    return True

CurentDir = os.getcwd()
EditorDir = CurentDir + "\\Edit"
WorkDir = CurentDir + "\\Client"
SaveDir = CurentDir + "\\Update/new"

# Выполняем функцию при запуске скрипта
prima = tkinter.Tk()
app = application(prima)
prima.mainloop()
