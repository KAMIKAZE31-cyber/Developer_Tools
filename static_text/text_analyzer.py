import tkinter as tk
from tkinter import ttk
import re

class TextAnalyzer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Анализатор текста")
        self.window.geometry("800x600")
        self.window.configure(bg='#f0f2f5')

        # Создаем основной контейнер
        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title = ttk.Label(
            self.main_frame,
            text="Анализатор текста",
            font=('Arial', 16, 'bold')
        )
        title.pack(pady=10)

        # Текстовое поле
        self.text_input = tk.Text(
            self.main_frame,
            height=10,
            width=50,
            font=('Arial', 12),
            wrap=tk.WORD
        )
        self.text_input.pack(pady=10, fill=tk.BOTH, expand=True)

        # Фрейм для статистики
        stats_frame = ttk.LabelFrame(self.main_frame, text="Статистика", padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем и размещаем метки для статистики
        self.stats_labels = {}
        stats = [
            "Всего символов", "Букв", "Заглавных букв",
            "Строчных букв", "Пробелов", "Специальных символов",
            "Цифр", "Слов"
        ]

        for i, stat in enumerate(stats):
            row = i // 2
            col = i % 2
            
            frame = ttk.Frame(stats_frame)
            frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            label = ttk.Label(frame, text=f"{stat}:")
            label.pack(side=tk.LEFT)
            
            value = ttk.Label(frame, text="0")
            value.pack(side=tk.RIGHT)
            
            self.stats_labels[stat] = value

        # Настраиваем равномерное распределение колонок
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)

        # Привязываем обработчик событий
        self.text_input.bind('<KeyRelease>', self.analyze_text)

    def analyze_text(self, event=None):
        text = self.text_input.get("1.0", tk.END)
        
        # Подсчет статистики
        stats = {
            "Всего символов": len(text) - 1,  # -1 для компенсации символа новой строки
            "Букв": len(re.findall(r'[a-zA-Zа-яА-ЯёЁ]', text)),
            "Заглавных букв": len(re.findall(r'[A-ZА-ЯЁ]', text)),
            "Строчных букв": len(re.findall(r'[a-zа-яё]', text)),
            "Пробелов": len(re.findall(r'\s', text)),
            "Специальных символов": len(re.findall(r'[^a-zA-Zа-яА-ЯёЁ\s\d]', text)),
            "Цифр": len(re.findall(r'\d', text)),
            "Слов": len(text.split()) if text.strip() else 0
        }

        # Обновляем метки
        for stat, value in stats.items():
            self.stats_labels[stat].configure(text=str(value))

    def run(self):
        # Настраиваем стиль
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TLabelframe', font=('Arial', 11))
        
        # Запускаем главный цикл
        self.window.mainloop()

if __name__ == "__main__":
    app = TextAnalyzer()
    app.run() 