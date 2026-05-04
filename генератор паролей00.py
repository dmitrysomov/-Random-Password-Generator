import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# --- Настройки ---
HISTORY_FILE = 'password_history.json'
MIN_LENGTH = 6
MAX_LENGTH = 32

# --- Функции логики ---

def generate_password(length, use_digits, use_letters, use_special):
    """Генерирует пароль на основе выбранных параметров."""
    chars = ''
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters
    if use_special:
        chars += string.punctuation

    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
        return ''

    return ''.join(random.choices(chars, k=length))

def save_history(password):
    """Сохраняет пароль в файл истории (JSON)."""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(password)

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_history(tree):
    """Загружает историю паролей из файла и отображает в таблице."""
    # Очищаем текущую таблицу
    for item in tree.get_children():
        tree.delete(item)

    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for pwd in data:
                tree.insert('', 'end', values=(pwd,))
    except (FileNotFoundError, json.JSONDecodeError):
        pass # Если файла нет или он пустой, просто ничего не делаем

# --- Функции интерфейса ---

def on_generate():
    """Обработчик нажатия кнопки 'Сгенерировать'."""
    length = int(scale_length.get())
    
    if length < MIN_LENGTH or length > MAX_LENGTH:
        messagebox.showerror("Ошибка", f"Длина пароля должна быть от {MIN_LENGTH} до {MAX_LENGTH} символов!")
        return

    password = generate_password(
        length,
        var_digits.get(),
        var_letters.get(),
        var_special.get()
    )
    
    if password: # Если генерация прошла успешно
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)
        save_history(password)
        load_history(tree_history) # Обновляем таблицу

# --- Создание окна ---

root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("500x450")
root.resizable(False, False)

# --- Блок настроек ---
settings_frame = tk.LabelFrame(root, text="Настройки генерации", padx=10, pady=10)
settings_frame.pack(pady=10, padx=15, fill="x")

# Длина пароля
tk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky='w')
scale_length = tk.Scale(settings_frame, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL, length=250)
scale_length.set(12)
scale_length.grid(row=0, column=1, columnspan=2, pady=(0, 10))

# Чекбоксы символов
var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)

tk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=var_digits).grid(row=1, column=0, sticky='w')
tk.Checkbutton(settings_frame, text="Буквы (a-zA-Z)", variable=var_letters).grid(row=1, column=1, sticky='w')
tk.Checkbutton(settings_frame, text="Спецсимволы (!@#$)", variable=var_special).grid(row=1, column=2, sticky='w')

# Кнопка генерации и поле результата
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Сгенерировать", command=on_generate).pack()

result_frame = tk.Frame(root)
result_frame.pack(pady=5)

tk.Label(result_frame, text="Ваш пароль:").pack(side="left")
entry_password = tk.Entry(result_frame, width=45)
entry_password.pack(side="left", padx=5)

# --- Блок истории ---
history_frame = tk.LabelFrame(root, text="История паролей", padx=10, pady=10)
history_frame.pack(pady=10, padx=15, fill="both", expand=True)

tree_history = ttk.Treeview(history_frame, columns=('password',), show='headings')
tree_history.heading('password', text='Сгенерированные пароли')
tree_history.column('password', minwidth=200, width=350, stretch=True)
tree_history.pack(fill="both", expand=True)

# Загрузка истории при старте приложения
if os.path.exists(HISTORY_FILE):
    load_history(tree_history)

# --- Запуск приложения ---
root.mainloop
