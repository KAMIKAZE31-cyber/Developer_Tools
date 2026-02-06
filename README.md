# Developer Tools 🛠️


Коллекция удобных онлайн-инструментов для разработчиков и IT-специалистов. Всё работает на Python/Django.

---

## 🚀 Features

- Множество утилит: Base64, генератор токенов, анализатор текста, конвертеры, работа с цветами и др.
- История использования инструментов
- Современный интерфейс (Django + HTML/CSS)
- Простая установка и запуск
- Открытый исходный код

---

## 📦 Installation

> Все команды выполняются в bash или WSL!

## 🐧 Установка и запуск на Linux и MacOS

```bash
# 1. Установите pip, если ещё не установлен
sudo apt install python3-pip         # Для Ubuntu/Debian
# или
brew install python3                 # Для MacOS (если не установлен Python3)

# 2. Клонируйте репозиторий
git clone https://github.com/Developer-Tools/Developer_Tools.git
cd Developer_Tools

# 3. Установите uv (опционально, если используете uv)
pip install uv

# 4. Создайте и активируйте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 5. Установите зависимости
pip install -r requirements.txt
pip install django pillow python-dotenv toml uv

# 6. Создайте .env и добавьте переменную:
# DJANGO_SECRET_KEY="ваш_секретный_ключ"

# 7. Миграции и запуск сервера
uv run manage.py migrate
uv run manage.py makemigrations
uv run manage.py runserver
```

---

## 🖥️ Usage

- Откройте браузер и перейдите по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Используйте инструменты через веб-интерфейс

---

## 📁 Project Structure

| Папка/файл         | Описание                        |
|--------------------|----------------------------------|
| `base64_tools/`    | Инструменты для Base64           |
| `color_HTML/`      | Работа с цветами                 |
| `converter_text/`  | Текстовые конвертеры             |
| `preobrazovarel/`  | Преобразователь текста           |
| `rimski_number/`   | Римские числа                    |
| `static_text/`     | Анализатор текста                |
| `token_generator/` | Генератор токенов                |
| `tools/`           | Главные шаблоны и страницы       |
| `history_files/`   | История использования            |
| `config/`          | Django-настройки                 |

---

## 🐳 Docker

### Быстрый старт через Docker Compose

1. Убедитесь, что установлен [Docker](  ) и [docker-compose](https://docs.docker.com/compose/).
2. В папке проекта выполните:
   ```bash
   docker-compose up --build
   # или (для новых версий Docker)
   docker compose up --build
   ```
3. Откройте [http://127.0.0.1:8000/](http://127.0.0.1:8000/) в браузере.

- Переменная `DJANGO_SECRET_KEY` задаётся в `docker-compose.yml` (замените на свой ключ).
- История и база данных сохраняются между перезапусками (volumes: `./history_files`, `./db.sqlite3`).
- Остановить проект: `docker-compose down`

---

## 📜 License

[MIT](LICENSE)

---

## ℹ️ About & Credits
Me :)




---


