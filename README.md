# TPPOSU

Версия python - 3.9.13

## Установка виртуального окружения
```
python -m venv venv
```
## Активация виртуального окружения
```
venv\Scripts\activate  # windows
```
## Установка зависимостей
ОБЯЗАТЕЛЬНО апдейт pip:
```
python -m pip install --upgrade pip
```
Установка:
```
pip install -r .\requirements.txt
```

## Запуск программы
```
python main.py
```

## Коммиты
Проверка изменений в главной ветке
```
git checkout main
git pull origin main
```

Переход на свою ветку
```
# Если ветки еще нет (создать и перейти):
git checkout -b имя-вашей-ветки #git checkout -b cpp_code

# Если ветка уже была создана ранее (просто перейти):
git checkout имя-вашей-ветки    #git checkout cpp_code
```

Создание коммита
```
git add .
git commit -m "Добавил фильтрацию в таблицу"
```

Пуш
```
git push origin имя-вашей-ветки #git push origin cpp_code
```
На GitHub открыть свой репозиторий, нажать Compare & pull request, описать изменений и Create pull request