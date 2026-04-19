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

class RegistrationSetupWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Параметры регистрации")
        self.geometry("400x300")
        
        self.attributes("-topmost", True)
        self.grab_set()
        self.after(100, self._center_window)

        ctk.CTkLabel(self, text="Настройка условий", font=("Arial", 16, "bold")).pack(pady=15)

        # --- Название эксперимента ---
        ctk.CTkLabel(self, text="Название эксперимента*:").pack()
        self.experiment_name_entry = ctk.CTkEntry(self, width=200)
        self.experiment_name_entry.pack(pady=(0, 10))
        
        # --- Количество кадров ---
        ctk.CTkLabel(self, text="Количество кадров:").pack()
        self.frames_entry = ctk.CTkEntry(self, width=200)
        self.frames_entry.insert(0, "100")
        self.frames_entry.pack(pady=(0, 10))

        self.btn_start = ctk.CTkButton(self, text="Начать регистрацию", command=self.start_action)
        self.btn_start.pack(pady=20)

    def _center_window(self):
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def start_action(self):
        # 1. Получаем значение и убираем лишние пробелы
        name = self.experiment_name_entry.get().strip()
        frames = self.frames_entry.get().strip()

        # 2. Проверка на пустоту
        if not name:
            # Подсвечиваем поле красным
            self.experiment_name_entry.configure(border_color="red", placeholder_text="Введите название!")
            self.experiment_name_entry.focus() # Возвращаем курсор в поле
            return # Прерываем выполнение функции, окно не закроется

        # 3. Если проверка прошла успешно
        # Сбрасываем цвет (на случай, если была ошибка ранее)
        self.experiment_name_entry.configure(border_color=["#979DA2", "#565B5E"]) 
        
        self.master.add_log(f"Запуск: '{name}', кадров: {frames}")
        self.destroy()

class AboutWindow(ctk.CTkToplevel):
    """Окно с информацией о программе"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("О программе")
        self.geometry("400x350")
        
        # Модальный режим
        self.attributes("-topmost", True)
        self.grab_set()
        self.resizable(False, False)
        self.after(100, self._center_window)

        # Логотип или Заголовок
        self.logo_label = ctk.CTkLabel(self, text="📊", font=("Arial", 60))
        self.logo_label.pack(pady=(20, 10))

        self.title_label = ctk.CTkLabel(self, text="Система регистрации и обработки данных", 
                                        font=("Arial", 18, "bold"))
        self.title_label.pack()

        # Описание
        description = (
            "Комплекс программных средств\n"
            "для регистрации и обработки данных измерений\n"
            "с объекта исследования\n"
        )
        self.desc_label = ctk.CTkLabel(self, text=description, font=("Arial", 13), justify="center")
        self.desc_label.pack(pady=20)

        # Информация об авторе/организации
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(pady=10)

        ctk.CTkLabel(self.info_frame, text="Разработчик:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, sticky="e")
        ctk.CTkLabel(self.info_frame, text="Бригада №1", font=("Arial", 12)).grid(row=0, column=1, padx=5, sticky="w")

        # Кнопка закрытия
        self.btn_close = ctk.CTkButton(self, text="Закрыть", width=100, command=self.destroy)
        self.btn_close.pack(pady=(20, 10))

    def _center_window(self):
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

class App(ctk.CTk):
    """Основное окно приложения"""
    def __init__(self):
        super().__init__()

        self.operator_name = "—"
        
        self.title("Система мониторинга")
        self.after(0, lambda: self.state('zoomed'))

        # Теперь 3 строки: 0-Панель, 1-Таблица (основная), 2-Журнал (снизу)
        self.grid_rowconfigure(1, weight=3) # Таблица больше
        self.grid_rowconfigure(2, weight=1) # Журнал меньше
        self.grid_columnconfigure(0, weight=1)

        # --- 1. ВЕРХНЯЯ ПАНЕЛЬ (без изменений) ---
        self.top_panel = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.top_panel.grid(row=0, column=0, sticky="nsew")

        self.button_container = ctk.CTkFrame(self.top_panel, fg_color="transparent")
        self.button_container.pack(side="left", padx=10)

        buttons = [
            ("Регистрация данных", self.open_registration_setup),
            ("Управление данными", None),
            ("Научно-технический расчет", None),
            ("О программе", self.open_about)
        ]

        for text, cmd in buttons:
            btn = ctk.CTkButton(self.button_container, text=text, width=150, command=cmd)
            btn.pack(side="left", padx=5, pady=10)

        self.operator_label = ctk.CTkLabel(self.top_panel, text=f"Оператор: {self.operator_name}", 
                                           font=("Arial", 14, "bold"))
        self.operator_label.pack(side="right", padx=20)

        # --- 2. ОБЛАСТЬ ТАБЛИЦЫ (Центр) ---
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="nsew")
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        self.data_view = ctk.CTkTextbox(self.table_frame, font=("Courier", 13))
        self.data_view.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.data_view.insert("0.0", "Ожидание данных...")
        self.data_view.configure(state="disabled")

        # --- 3. ЖУРНАЛ СОБЫТИЙ (Низ) ---
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")
        
        # Заголовок журнала и кнопка очистки
        self.log_header = ctk.CTkFrame(self.log_frame, fg_color="transparent", height=10)
        self.log_header.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.log_header, text="Журнал событий", font=("Arial", 12, "bold")).pack(side="left")
        self.btn_clear_logs = ctk.CTkButton(self.log_header, text="Очистить", width=80, height=24, 
                                            fg_color="gray", hover_color="#666666", command=self.clear_logs)
        self.btn_clear_logs.pack(side="right")

        # Поле вывода логов
        self.log_view = ctk.CTkTextbox(self.log_frame, font=("Courier", 12), height=10)
        self.log_view.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_view.configure(state="disabled")

        self.ask_user_info()

    # --- МЕТОДЫ ---

    def add_log(self, message):
        """Добавляет запись в журнал с отметкой времени"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_view.configure(state="normal")
        self.log_view.insert("end", f"[{timestamp}] {message}\n")
        self.log_view.see("end") # Прокрутка вниз
        self.log_view.configure(state="disabled")

    def clear_logs(self):
        """Очистка журнала"""
        self.log_view.configure(state="normal")
        self.log_view.delete("1.0", "end")
        self.log_view.configure(state="disabled")

    def open_registration_setup(self):
        RegistrationSetupWindow(self)

    def update_operator_info(self):
        self.operator_label.configure(text=f"Оператор: {self.operator_name}")
        self.add_log(f"Оператор {self.operator_name} вошел в систему")

    def ask_user_info(self):
        self.after(200, lambda: LoginWindow(self))

    def open_about(self):
        """Открывает окно О программе"""
        AboutWindow(self)
        self.add_log("Открыто окно 'О программе'")