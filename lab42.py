# lab42.py
from tkinter import *
from tkinter import messagebox
import os
from list_adapter import CPPBackend, PythonBackend


class ListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Двусвязный список")
        self.root.geometry("450x500")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Текущий бэкенд и язык
        self.backend = None
        self.current_lang = StringVar(value="cpp")
        self.list_handle = None

        self._setup_ui()
        self._switch_backend()  # Инициализация при запуске

    def _setup_ui(self):
        # === Панель выбора языка ===
        lang_frame = Frame(self.root, pady=5)
        lang_frame.pack(fill=X)
        Label(lang_frame, text="Бэкенд:").pack(side=LEFT, padx=5)
        Radiobutton(lang_frame, text="C++", variable=self.current_lang,
                    value="cpp", command=self._switch_backend).pack(side=LEFT)
        Radiobutton(lang_frame, text="Python", variable=self.current_lang,
                    value="py", command=self._switch_backend).pack(side=LEFT)

        # === Поля ввода ===
        input_frame = Frame(self.root, padx=10, pady=5)
        input_frame.pack(fill=X)

        Label(input_frame, text="Индекс:").grid(row=0, column=0, sticky="w")
        self.index_input = Entry(input_frame, width=10)
        self.index_input.grid(row=0, column=1, padx=5, sticky="w")

        Label(input_frame, text="Значение:").grid(row=1, column=0, sticky="w")
        self.data_input = Entry(input_frame)
        self.data_input.grid(row=1, column=1, padx=5, sticky="we")
        input_frame.columnconfigure(1, weight=1)

        # === Список ===
        self.listbox = Listbox(self.root, height=12)
        self.listbox.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # === Кнопки ===
        btn_frame = Frame(self.root, pady=5)
        btn_frame.pack()
        Button(btn_frame, text="➕ Добавить", command=self.add_item, width=12).pack(side=LEFT, padx=5)
        Button(btn_frame, text="🗑️ Удалить", command=self.remove_item, width=12).pack(side=LEFT, padx=5)
        Button(btn_frame, text="🔄 Обновить", command=self.update_listbox, width=12).pack(side=LEFT, padx=5)

        # === Статус ===
        self.status_var = StringVar(value="Готово")
        Label(self.root, textvariable=self.status_var, bd=1, relief=SUNKEN, anchor="w").pack(fill=X, side=BOTTOM)

    def _switch_backend(self):
        """Переключение между бэкендами с сохранением данных (опционально)"""
        # Сохраняем текущие данные (если нужно)
        old_data = []
        if self.list_handle and self.backend:
            count = self.backend.get_count()
            for i in range(count):
                val = self.backend.get_element(i)
                if val is not None:
                    old_data.append(val)
            self.backend.free()

        # Создаём новый бэкенд
        if self.current_lang.get() == "cpp":
            lib_path = os.path.join(os.path.dirname(__file__), "liblist.dylib")
            self.backend = CPPBackend(lib_path)
        else:
            self.backend = PythonBackend()

        self.list_handle = self.backend.create()
        self.status_var.set(f"Бэкенд: {self.current_lang.get().upper()}")

        # Восстанавливаем данные (опционально)
        for val in old_data:
            try:
                self.backend.insert(self.backend.get_count(), val)
            except:
                pass  # Если не удалось — пропускаем

        self.update_listbox()

    def update_listbox(self):
        """Обновление отображения списка"""
        self.listbox.delete(0, END)
        if not self.backend:
            return
        count = self.backend.get_count()
        if count == 0:
            self.listbox.insert(END, "📭 Список пуст")
            return
        for i in range(count):
            val = self.backend.get_element(i)
            self.listbox.insert(END, f"{i}: {val}")

    def add_item(self):
        """Добавление элемента"""
        try:
            index = int(self.index_input.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовой индекс!")
            return

        data = self.data_input.get().strip()
        if not data:
            messagebox.showerror("Ошибка", "Введите значение!")
            return

        try:
            count = self.backend.get_count()
            if index < 0 or index > count:
                raise IndexError
            self.backend.insert(index, data)
            self.update_listbox()
            self.data_input.delete(0, END)
            self.index_input.delete(0, END)
            self.status_var.set(f"Добавлено: '{data}'")
        except IndexError:
            messagebox.showerror("Ошибка", f"Индекс должен быть от 0 до {count}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def remove_item(self):
        """Удаление элемента"""
        try:
            index = int(self.index_input.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовой индекс!")
            return

        try:
            count = self.backend.get_count()
            if count == 0:
                raise Exception("Список пуст")
            if index < 0 or index >= count:
                raise IndexError
            self.backend.delete(index)
            self.update_listbox()
            self.index_input.delete(0, END)
            self.status_var.set(f"Удалено индекс {index}")
        except IndexError:
            messagebox.showerror("Ошибка", f"Индекс должен быть от 0 до {count - 1}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_closing(self):
        """Корректное завершение"""
        if self.backend:
            self.backend.free()
        self.root.destroy()


# === Запуск ===
if __name__ == "__main__":
    root = Tk()
    app = ListApp(root)
    root.mainloop()