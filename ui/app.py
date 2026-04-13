import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.title("Система мониторинга датчиков")
        self.geometry("900x500")

        # Конфигурация сетки (2 колонки: боковая панель и основная часть)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Боковая панель (Управление) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Управление", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_refresh = ctk.CTkButton(self.sidebar_frame, text="Обновить данные", command=self.refresh_data)
        self.btn_refresh.grid(row=1, column=0, padx=20, pady=10)

        self.btn_export = ctk.CTkButton(self.sidebar_frame, text="Экспорт в Excel", fg_color="transparent", border_width=2)
        self.btn_export.grid(row=2, column=0, padx=20, pady=10)

        # --- Основная область (Таблица/Графики) ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        self.status_label = ctk.CTkLabel(self.main_content, text="Последние данные из БД", font=ctk.CTkFont(size=16))
        self.status_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Заглушка под таблицу (позже заменим на CTkTable)
        self.data_display = ctk.CTkTextbox(self.main_content, activate_scrollbars=True)
        self.data_display.grid(row=1, column=0, sticky="nsew")
        self.data_display.insert("0.0", "Здесь будут отображаться данные от C++ имитатора...")

    def refresh_data(self):
        # Метод для будущего вызова из database.py
        print("Запрос к базе данных...")
        self.data_display.insert("end", "\nОбновление данных...")