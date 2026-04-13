import customtkinter as ctk

class LoginWindow(ctk.CTkToplevel):
    """Мини-окно для ввода ФИО оператора"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Авторизация")
        self.geometry("350x200")
        
        # Поверх всех окон и блокировка основного окна
        self.attributes("-topmost", True)
        self.after(100, self._center_window)
        self.grab_set()

        # Элементы интерфейса
        self.label = ctk.CTkLabel(self, text="Введите ФИО оператора", font=("Arial", 14))
        self.label.pack(pady=(30, 10))

        self.entry = ctk.CTkEntry(self, placeholder_text="Иванов И.И.", width=220)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda e: self.submit()) # Вход по Enter

        self.btn_submit = ctk.CTkButton(self, text="Войти", command=self.submit)
        self.btn_submit.pack(pady=20)

        # Если закрыли окно крестиком, закрываем всё приложение
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def submit(self):
        name = self.entry.get().strip()
        if name:
            self.parent.operator_name = name
            self.parent.update_operator_info()
            self.destroy()
        else:
            self.entry.configure(placeholder_text_color="red", border_color="red")

    def on_closing(self):
        self.parent.destroy()


class App(ctk.CTk):
    """Основное окно приложения"""
    def __init__(self):
        super().__init__()

        self.operator_name = "—"
        
        # Настройка полноэкранного режима
        self.title("Система мониторинга")
        self.after(0, lambda: self.state('zoomed'))

        # Сетка: Строка 0 (Панель), Строка 1 (Таблица)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- ВЕРХНЯЯ ПАНЕЛЬ (Управление) ---
        self.top_panel = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.top_panel.grid(row=0, column=0, sticky="nsew")

        # 1. Контейнер для кнопок (слева)
        self.button_container = ctk.CTkFrame(self.top_panel, fg_color="transparent")
        self.button_container.pack(side="left", padx=10)

        for btn_text in ["Считать", "Фильтр", "Анализ", "Экспорт"]:
            btn = ctk.CTkButton(self.button_container, text=btn_text, width=100)
            btn.pack(side="left", padx=5, pady=10)

        # 2. Метка оператора (справа)
        self.operator_label = ctk.CTkLabel(self.top_panel, text=f"Оператор: {self.operator_name}", 
                                           font=("Arial", 14, "bold"))
        self.operator_label.pack(side="right", padx=20)

        # --- ОБЛАСТЬ ТАБЛИЦЫ ---
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        # Заглушка (позже заменим на CTkTable)
        self.data_view = ctk.CTkTextbox(self.table_frame, font=("Courier", 13))
        self.data_view.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.data_view.insert("0.0", "Ожидание данных...")
        self.data_view.configure(state="disabled")

        # Запуск окна авторизации
        self.ask_user_info()

    def ask_user_info(self):
        # Используем after, чтобы основное окно успело проинициализироваться
        self.after(200, lambda: LoginWindow(self))

    def update_operator_info(self):
        """Обновление ФИО в интерфейсе"""
        self.operator_label.configure(text=f"Оператор: {self.operator_name}")
