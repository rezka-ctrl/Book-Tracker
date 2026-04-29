import tkinter as tk
from tkinter import ttk, messagebox

from validator import validate_pages, validate_not_empty
from storage import load_data, save_data

GENRES = ["Фантастика", "Роман", "Детектив", "История", "Наука", "Поэзия", "Биография", "Другое"]
MIN_PAGES_FILTER_DEFAULT = ""


def on_add():
    """Обработчик кнопки «Добавить книгу»: валидирует и сохраняет запись."""
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_combo.get().strip()
    pages = pages_entry.get().strip()

    if not validate_not_empty(title):
        messagebox.showerror("Ошибка", "Название книги не может быть пустым.")
        return
    if not validate_not_empty(author):
        messagebox.showerror("Ошибка", "Имя автора не может быть пустым.")
        return
    if not validate_not_empty(genre):
        messagebox.showerror("Ошибка", "Выберите жанр.")
        return
    if not pages:
        messagebox.showerror("Ошибка", "Введите количество страниц.")
        return
    if not validate_pages(pages):
        messagebox.showerror("Ошибка", "Количество страниц должно быть положительным целым числом.")
        return

    record = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages),
    }
    all_records.append(record)
    save_data(all_records)
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)
    apply_filter()


def apply_filter():
    """Применяет фильтр по жанру и минимальному количеству страниц."""
    genre_filter = filter_genre_combo.get()
    pages_filter = filter_pages_entry.get().strip()

    filtered = all_records[:]
    if genre_filter and genre_filter != "Все":
        filtered = [r for r in filtered if r["genre"] == genre_filter]
    if pages_filter:
        try:
            min_pages = int(pages_filter)
            filtered = [r for r in filtered if r["pages"] > min_pages]
        except ValueError:
            messagebox.showerror("Ошибка", "Фильтр страниц должен быть целым числом.")
            return

    refresh_table(filtered)


def clear_filter():
    """Сбрасывает фильтры."""
    filter_genre_combo.set("Все")
    filter_pages_entry.delete(0, tk.END)
    refresh_table(all_records)


def refresh_table(records):
    """Перерисовывает таблицу книг."""
    for row in tree.get_children():
        tree.delete(row)
    for rec in records:
        tree.insert("", tk.END, values=(rec["title"], rec["author"], rec["genre"], rec["pages"]))


# ── Главное окно ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Book Tracker — Трекер прочитанных книг")
root.geometry("720x620")
root.resizable(False, False)

# ── Форма добавления ──────────────────────────────────────────────────────────
form = tk.LabelFrame(root, text="Добавить книгу", padx=10, pady=8)
form.pack(fill=tk.X, padx=12, pady=8)

labels = ["Название книги:", "Автор:", "Жанр:", "Количество страниц:"]
for i, lbl in enumerate(labels):
    tk.Label(form, text=lbl).grid(row=i, column=0, sticky=tk.W, pady=3)

title_entry = tk.Entry(form, width=34)
title_entry.grid(row=0, column=1, sticky=tk.W, padx=6)

author_entry = tk.Entry(form, width=34)
author_entry.grid(row=1, column=1, sticky=tk.W, padx=6)

genre_combo = ttk.Combobox(form, values=GENRES, state="readonly", width=32)
genre_combo.grid(row=2, column=1, sticky=tk.W, padx=6)

pages_entry = tk.Entry(form, width=14)
pages_entry.grid(row=3, column=1, sticky=tk.W, padx=6)

tk.Button(
    form, text="➕  Добавить книгу", command=on_add,
    bg="#795548", fg="white", padx=12, pady=4,
).grid(row=4, column=0, columnspan=2, pady=8)

# ── Фильтр ────────────────────────────────────────────────────────────────────
flt = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=6)
flt.pack(fill=tk.X, padx=12, pady=4)

tk.Label(flt, text="Жанр:").grid(row=0, column=0, sticky=tk.W)
filter_genre_combo = ttk.Combobox(flt, values=["Все"] + GENRES, state="readonly", width=16)
filter_genre_combo.set("Все")
filter_genre_combo.grid(row=0, column=1, padx=6)

tk.Label(flt, text="Страниц больше:").grid(row=0, column=2, sticky=tk.W, padx=(12, 0))
filter_pages_entry = tk.Entry(flt, width=10)
filter_pages_entry.grid(row=0, column=3, padx=6)

tk.Button(flt, text="Применить", command=apply_filter, padx=8).grid(row=0, column=4, padx=4)
tk.Button(flt, text="Сбросить", command=clear_filter, padx=8).grid(row=0, column=5, padx=4)

# ── Таблица ───────────────────────────────────────────────────────────────────
tbl_frm = tk.LabelFrame(root, text="Список книг", padx=8, pady=6)
tbl_frm.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

columns = ("Название", "Автор", "Жанр", "Страниц")
tree = ttk.Treeview(tbl_frm, columns=columns, show="headings", height=12)
for col, w in zip(columns, [240, 180, 130, 80]):
    tree.heading(col, text=col)
    tree.column(col, width=w, anchor=tk.CENTER)

sb = ttk.Scrollbar(tbl_frm, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=sb.set)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
sb.pack(side=tk.RIGHT, fill=tk.Y)

# ── Загрузка данных ───────────────────────────────────────────────────────────
all_records = load_data()
refresh_table(all_records)

root.mainloop()
