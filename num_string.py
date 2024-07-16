import os

from settings import ROOT_DIRECTORY


def count_lines_in_files(directory, extensions, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = []

    total_lines = 0
    for root, dirs, files in os.walk(directory):
        # Пропускаем директории, которые хотим исключить из подсчета
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            if any(file.endswith(ext) for ext in extensions):
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
    return total_lines


root_directory = ROOT_DIRECTORY
extensions = ['.py', '.html', '.js']  # Список расширений файлов
exclude_dirs = ['.venv', 'development', 'templates', 'static']  # Список директорий для исключения
total_lines = count_lines_in_files(root_directory, extensions, exclude_dirs)
print(f"Всего строк кода: {total_lines}")

# 1231 04/07/24
# 1526 16/07/24
