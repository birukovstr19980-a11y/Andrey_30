import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("650x650")
        # Установка фонового цвета окна
        self.root.configure(bg="#f0f8ff")  # Alice Blue

        # База данных (Пункт 1)
        self.quotes = [
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон",
             "theme": "Жизнь"},
            {"text": "Успех — это идти от ошибки к ошибке, не теряя энтузиазма.", "author": "Уинстон Черчилль",
             "theme": "Успех"},
            {"text": "Свобода ничего не стоит, если она не включает в себя свободу ошибаться.",
             "author": "Махатма Ганди", "theme": "Свобода"}
        ]

        self.history = []
        self.load_history()  # Загрузка истории (Пункт 5)

        self.setup_ui()

    def setup_ui(self):
        # Отображение цитаты с новыми параметрами цвета и шрифта
        self.quote_label = tk.Label(self.root, text="Нажмите кнопку ниже",
                                    wraplength=500,
                                    font=("Georgia", 14, "bold italic"),  # Шрифт изменён на Georgia, увеличен размер, добавлен жирный курсив
                                    fg="#2e8b57",  # Цвет текста — морской зелёный
                                    bg="#f0f8ff",  # Фон совпадает с фоном окна
                                    justify="center")  # Выравнивание по центру
        self.quote_label.pack(pady=20)

        # Кнопка генерации (Пункт 2) с улучшенным дизайном
        btn_gen = tk.Button(self.root,
                           text="Сгенерировать цитату",
                           command=self.generate_quote,
                           bg="#4682b4",  # Стальной синий
                           fg="white",  # Белый текст
                           font=("Helvetica", 11, "bold"),  # Шрифт и размер
                           relief="raised",  # Объёмная кнопка
                           bd=3)  # Толщина границы
        btn_gen.pack(pady=5)

        # --- СЕКЦИЯ ДОБАВЛЕНИЯ (Пункт 6) ---
        add_frame = tk.LabelFrame(self.root,
                                text="Добавить свою цитату",
                                bg="#f0f8ff",  # Цвет фона рамки
                                fg="#4682b4")  # Цвет заголовка рамки
        add_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(add_frame, text="Текст:", bg="#f0f8ff", fg="#2e8b57", font=("Arial", 10)).grid(row=0, column=0)
        self.entry_text = tk.Entry(add_frame, width=50, font=("Arial", 10))
        self.entry_text.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(add_frame, text="Автор:", bg="#f0f8ff", fg="#2e8b57", font=("Arial", 10)).grid(row=1, column=0)
        self.entry_author = tk.Entry(add_frame, width=50, font=("Arial", 10))
        self.entry_author.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(add_frame, text="Тема:", bg="#f0f8ff", fg="#2e8b57", font=("Arial", 10)).grid(row=2, column=0)
        self.entry_theme = tk.Entry(add_frame, width=50, font=("Arial", 10))
        self.entry_theme.grid(row=2, column=1, padx=5, pady=2)

        btn_add = tk.Button(add_frame,
                          text="Добавить в базу",
                          command=self.add_custom_quote,
                          bg="#32cd32",  # Лаймовый зелёный
                          fg="white",
                          font=("Helvetica", 10, "bold"))
        btn_add.grid(row=3, column=0, columnspan=2, pady=5)

        # --- ФИЛЬТРАЦИЯ (Пункт 4) ---
        filter_frame = tk.Frame(self.root, bg="#f0f8ff")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame,
                text="Поиск в истории (Автор/Тема):",
                bg="#f0f8ff",
                fg="#4682b4",
                font=("Arial", 10)).pack(side=tk.LEFT)
        self.filter_entry = tk.Entry(filter_frame, font=("Arial", 10))
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        self.filter_entry.bind("<KeyRelease>", lambda event: self.apply_filter())  # Живой поиск

        # --- ИСТОРИЯ (Пункт 3) ---
        tk.Label(self.root,
                text="История сгенерированных цитат:",
                bg="#f0f8ff",
                fg="#4682b4",
                font=("Helvetica", 12, "bold")).pack()
        self.history_listbox = tk.Listbox(self.root,
                                         width=80,
                                         height=8,
                                         font=("Courier New", 9),  # Моноширинный шрифт для истории
                                         bg="#ffffff",  # Белый фон
                                         fg="#000000")  # Чёрный текст
        self.history_listbox.pack(pady=5, padx=10)
        self.update_history_display()

    # ПУНКТ 6: Проверка корректности ввода
    def add_custom_quote(self):
        text = self.entry_text.get()
        author = self.entry_author.get()
        theme = self.entry_theme.get()

        if not text.strip() or not author.strip() or not theme.strip():
            messagebox.showwarning("Внимание", "Поля не могут быть пустыми!")
            return

        new_q = {"text": text, "author": author, "theme": theme}
        self.quotes.append(new_q)

        # Очистка полей после добавления
        self.entry_text.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_theme.delete(0, tk.END)
        messagebox.showinfo("Успех", "Цитата успешно добавлена в список!")

    def generate_quote(self):
        if not self.quotes:
            return
        quote = random.choice(self.quotes)
        self.quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]} ({quote["theme"]})')

        self.history.append(quote)
        self.save_history()  # Пункт 5
        self.update_history_display()

    def update_history_display(self, items=None):
        self.history_listbox.delete(0, tk.END)
        display_items = items if items is not None else self.history
        for q in reversed(display_items):  # Новые сверху
            self.history_listbox.insert(tk.END, f"[{q['theme']}] {q['author']}: {q['text']}")

    def apply_filter(self):
        query = self.filter_entry.get().lower()
        filtered = [q for q in self.history if query in q['author'].lower() or query in q['theme'].lower()]
        self.update_history_display(filtered)

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)
    def load_history(self):
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except:
                self.history = []


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()

