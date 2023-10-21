import subprocess

subprocess.check_call(["python", '-m', 'pip', 'install', 'gitpython'])

import os
import shutil
from git import Repo

# Создаем объект репозитория
repo = Repo('.')

# Получаем имя текущей ветки
current_branch = repo.active_branch.name

# Создаем папку 'data/celebrates' в текущей ветке
os.makedirs('data/celebrates', exist_ok=True)

# Переключаемся на ветку 'main' (из которой хотим скопировать папку)
repo.git.checkout('main')

# Получаем список файлов в папке 'data/celebrates'
files = os.listdir('data/celebrates')

# Копируем каждый файл в 'data/celebrates' текущей ветки
for file in files:
    shutil.copy(os.path.join('data/celebrates', file), os.path.join('..', current_branch, 'data/celebrates'))

# Переключаемся на ветку из которой мы ушли
repo.git.checkout(current_branch)

# Делаем коммит
repo.git.add('data/celebrates/*')
repo.git.commit('-m', 'Copied files to data/celebrates')

# Пушим изменения в удаленный репозиторий
repo.git.push('origin', current_branch)