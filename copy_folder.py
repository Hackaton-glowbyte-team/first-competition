import subprocess

subprocess.check_call(["python", '-m', 'pip', 'install', 'gitpython'])

from git import Repo

# Создаем объект репозитория
repo = Repo('.')

# Получаем имя текущей ветки
current_branch = repo.active_branch.name

# Переключаемся на ветку 'main' (из которой хотим скопировать папку)
repo.git.checkout('main')

# Копируем папку
repo.git.checkout(current_branch, 'data/celebrates')

# Переключаемся на ветку из которой мы ушли
repo.git.checkout(current_branch)

# Делаем коммит
repo.git.commit('-m', 'Moved folder_to_move to new location')

# Пушим изменения в удаленный репозиторий
repo.git.push('origin', current_branch)