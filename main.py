import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# --- 1. Конфигурация и работа с данными (JSON) ---
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "history.json")

def ensure_data_dir_exists():
    """Создает каталог 'data', если его нет на диске."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        # Создаем пустой файл истории, чтобы избежать ошибок при чтении
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

def load_history():
    """Загружает историю сгенерированных задач из файла JSON."""
    ensure_data_dir_exists()
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_history(history_list):
    """Сохраняет историю задач в файл JSON."""
    ensure_data_dir_exists()
    with open(DATA_FILE, "w") as file:
        json.dump(history_list, file, indent=4)


# --- 2. Логика приложения (Класс App) ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Random Task Generator")
        self.geometry("600x500")
        self.resizable(False, False)
        self.configure(bg="#f0f8ff") # Светло-голубой фон

        # Инициализация данных
        self.default_tasks = {
            "Учёба": ["Прочитать статью", "Решить 5 задач", "Посмотреть лекцию"],
            "Спорт": ["Сделать зарядку", "Пробежать 1 км", "Посетить спортзал"],
            "Работа": ["Написать отчет", "Провести созвон", "Разобрать почту"]
        }
        
        self.all_tasks = [task for tasks in self.default_tasks.values() for task in tasks]
        
        self.history = load_history()
        
        self.create_widgets()
        self.update_history_display()

    def create_widgets(self):
        # --- Верхний фрейм: Фильтр и Генерация ---
        top_frame = tk.Frame(self, bg="#f0f8ff")
        top_frame.pack(pady=10, fill="x", padx=20)

        # Фильтр по типу задачи
        tk.Label(top_frame, text="Категория:", bg="#f0f8ff").pack(side="left")
        
        self.filter_var = tk.StringVar(value="Все")
        filter_options = ["Все"] + list(self.default_tasks.keys())
        
        self.filter_dropdown = ttk.Combobox(
            top_frame, 
            textvariable=self.filter_var, 
            values=filter_options, 
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        self.filter_dropdown.pack(side="left", padx=5)

        # Кнопка Генерации
        btn_generate = tk.Button(
            top_frame,
            text="Сгенерировать задачу",
            command=self.generate_task,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            width=20,
        )
        btn_generate.pack(side="left", padx=20)


        # --- Центральный фрейм: Текущая задача ---
        task_frame = tk.Frame(self, bg="#f0f8ff")
        task_frame.pack(pady=15, fill="x", padx=20)
        
        tk.Label(task_frame, text="Ваша задача:", font=("Arial", 12, 'bold'), bg="#f0f8ff").pack()
        self.current_task_label = tk.Label(
            task_frame,
            text="Нажмите кнопку, чтобы начать",
            font=("Arial", 14),
            wraplength=300,
            bg="#e0f7fa",
            relief="solid",
            width=40,
            height=3
        )
        self.current_task_label.pack(pady=10)


        # --- Нижний фрейм: История и Добавление задачи ---
        bottom_frame = tk.Frame(self, bg="#f0f8ff")
        bottom_frame.pack(pady=10, fill="both", expand=True, padx=20)

        # Левая часть: История задач
        history_frame = tk.LabelFrame(bottom_frame, text="История задач", bg="#f0f8ff")
        history_frame.pack(side="left", fill="both", expand=True)
        
        self.history_listbox = tk.Listbox(
            history_frame,
            font=("Arial", 10),
            height=12,
            bg="white"
        )
        self.history_listbox.pack(fill="both", expand=True)
        
        btn_save_history = tk.Button(
            history_frame,
            text="Сохранить историю",
            command=lambda: save_history(self.history),
            bg="#FF9800",
            fg="white"
        )
        btn_save_history.pack(pady=5)


        # Правая часть: Добавление новой задачи
        add_frame = tk.LabelFrame(bottom_frame, text="Добавить свою задачу", bg="#f0f8ff")
        add_frame.pack(side="right", fill="y")
        
        tk.Label(add_frame, text="Задача:", bg="#f0f8ff").pack(pady=5)
        self.new_task_entry = tk.Entry(add_frame, font=("Arial", 10), width=25)
        self.new_task_entry.pack(pady=5)
        
        tk.Label(add_frame, text="Категория:", bg="#f0f8ff").pack()
        self.category_var = tk.StringVar(value="Учёба")
        category_options = list(self.default_tasks.keys())
        
        self.category_dropdown = ttk.Combobox(
            add_frame, 
            textvariable=self.category_var, 
            values=category_options, 
            state="readonly",
            width=23,
            font=("Arial", 10)
        )
        self.category_dropdown.pack(pady=5)
        
        btn_add_task = tk.Button(
            add_frame,
            text="Добавить в список",
            command=self.add_custom_task,
            bg="#2196F3",
            fg="white"
        )
        btn_add_task.pack(pady=15)

    def generate_task(self):
        """Генерирует случайную задачу на основе выбранного фильтра."""
        selected_filter = self.filter_var.get()
        
        if selected_filter == "Все":
            task_pool = self.all_tasks
        else:
            task_pool = self.default_tasks.get(selected_filter, [])
            
        if not task_pool:
            messagebox.showwarning("Нет задач", f"В категории '{selected_filter}' нет доступных задач.")
            return

        task = random.choice(task_pool)
        
        # Отображение текущей задачи
        self.current_task_label.config(text=task)
        
        # Добавление в историю
        self.history.append(task)
        self.update_history_display()

    def update_history_display(self):
        """Обновляет виджет Listbox с историей задач."""
        self.history_listbox.delete(0, tk.END) # Очищаем список
        
        if not self.history:
            return
            
        for task in reversed(self.history): # Показываем последние задачи сверху
            self.history_listbox.insert(0, task)

    def add_custom_task(self):
        """Добавляет новую задачу, введенную пользователем."""
        task_text = self.new_task_entry.get().strip()
        
        # Валидация ввода (не пустая строка)
        if not task_text:
            messagebox.showwarning("Ошибка ввода", "Поле задачи не должно быть пустым!")
            return

        category = self.category_var.get()
        
        # Добавление в словарь и общий список
        if category not in self.default_tasks:
            self.default_tasks[category] = []
            
        self.default_tasks[category].append(task_text)
        self.all_tasks.append(task_text)
        
        messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена в категорию '{category}'.")
        
        # Очистка полей ввода
        self.new_task_entry.delete(0, tk.END)


# --- 3. Точка входа ---
if __name__ == '__main__':
    app = App()
    app.mainloop()
