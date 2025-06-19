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

```bash
# Установите pip, если ещё не установлен
sudo apt install python3-pip

# Клонируйте репозиторий
git clone https://github.com/Developer-Tools/Developer_Tools.git
cd Developer_Tools

# Установка uv
pip install uv

# Создайте и активируйте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
pip install django pillow python-dotenv toml uv

# Создайте .env и добавьте переменную:
# DJANGO_SECRET_KEY="ваш_секретный_ключ"

# Миграции и запуск сервера
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


---

## 📜 License

[MIT](LICENSE)

---

## ℹ️ About & Credits



---


