import tkinter as tk
from tkinter import ttk, messagebox

def to_roman(number):
    if not 0 < number < 4000:
        return "Число должно быть от 1 до 3999"
    
    roman_values = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I")
    ]
    
    result = ""
    for value, numeral in roman_values:
        while number >= value:
            result += numeral
            number -= value
    return result

def convert():
    try:
        number = int(entry.get())
        if 0 < number < 4000:
            result = to_roman(number)
            roman_result.set(result)
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите число от 1 до 3999")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число")

# Создание главного окна
root = tk.Tk()
root.title("Конвертер римских чисел")
root.geometry("400x200")

# Настройка стиля
style = ttk.Style()
style.configure("TLabel", padding=5, font=('Arial', 12))
style.configure("TEntry", padding=5, font=('Arial', 12))
style.configure("TButton", padding=5, font=('Arial', 12))

# Создание и размещение элементов интерфейса
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Введите число (1-3999):").grid(row=0, column=0, pady=5)
entry = ttk.Entry(frame, width=20)
entry.grid(row=0, column=1, pady=5)

ttk.Button(frame, text="Конвертировать", command=convert).grid(row=1, column=0, columnspan=2, pady=10)

ttk.Label(frame, text="Римское число:").grid(row=2, column=0, pady=5)
roman_result = tk.StringVar()
ttk.Label(frame, textvariable=roman_result).grid(row=2, column=1, pady=5)

# Центрирование окна
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# Запуск приложения
root.mainloop() 