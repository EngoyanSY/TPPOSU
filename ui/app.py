import customtkinter as ctk
import tksheet
import random
from datetime import datetime
from sqlmodel import Session

from ui.database import Experiments, Measurements, engine


class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Авторизация")
        self.geometry("350x200")
        self.attributes("-topmost", True)
        self.after(100, self._center_window)
        self.grab_set()

        ctk.CTkLabel(self, text="Введите ФИО оператора", font=("Arial", 14)).pack(pady=(30, 10))
        self.entry = ctk.CTkEntry(self, placeholder_text="Иванов И.И.", width=220)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda e: self.submit())

        ctk.CTkButton(self, text="Войти", command=self.submit).pack(pady=20)
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
            self.entry.configure(border_color="red")

    def on_closing(self):
        self.parent.destroy()


class RegistrationSetupWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Параметры регистрации")
        self.geometry("460x400")
        self.attributes("-topmost", True)
        self.grab_set()
        self.after(100, self._center_window)

        ctk.CTkLabel(self, text="Настройка условий", font=("Arial", 16, "bold")).pack(pady=15)

        ctk.CTkLabel(self, text="Название эксперимента*:").pack(anchor="w", padx=30)
        self.experiment_name_entry = ctk.CTkEntry(self, width=340)
        self.experiment_name_entry.pack(pady=(5, 15), padx=30)

        ctk.CTkLabel(self, text="Количество кадров:").pack(anchor="w", padx=30)
        self.frames_entry = ctk.CTkEntry(self, width=340)
        self.frames_entry.insert(0, "2000")
        self.frames_entry.pack(pady=(5, 20), padx=30)

        self.btn_start = ctk.CTkButton(self, text="Начать регистрацию", 
                                       command=self.start_action, height=40)
        self.btn_start.pack(pady=10)

        # Область загрузки
        self.loading_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.loading_label = ctk.CTkLabel(self.loading_frame, text="", font=("Arial", 13))
        self.loading_label.pack(pady=(0, 8))
        self.progress_bar = ctk.CTkProgressBar(self.loading_frame, width=340, height=12)
        self.progress_bar.pack()
        self.progress_bar.set(0)
        self.loading_frame.pack_forget()

    def _center_window(self):
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def start_action(self):
        name = self.experiment_name_entry.get().strip()
        frames_raw = self.frames_entry.get().strip()

        if not name:
            self.experiment_name_entry.configure(border_color="red")
            return
        if not frames_raw.isdigit() or int(frames_raw) < 1:
            self.frames_entry.configure(border_color="red")
            return

        n_frames = int(frames_raw)

        with Session(engine) as session:
            new_experiment = Experiments(
                name=name,
                operator=self.master.operator_name
            )
            session.add(new_experiment)
            session.commit()
            session.refresh(new_experiment)

            # сохраняем id, чтобы потом привязать измерения
            self.experiment_id = new_experiment.id

        self.master.add_log(f"Эксперимент '{name}' создан (ID={self.experiment_id})")

        self.experiment_name_entry.configure(border_color=["#979DA2", "#565B5E"])
        self.frames_entry.configure(border_color=["#979DA2", "#565B5E"])

        self.loading_frame.pack(fill="x", padx=30, pady=15)
        self.loading_label.configure(text="Генерация данных...")
        self.progress_bar.set(0)
        self.btn_start.configure(state="disabled", text="Идёт генерация...")

        self.after(50, lambda: self._run_generation(name, n_frames))

        with Session(engine) as session:
            exp = session.get(Experiments, self.experiment_id)
            exp.end_time = datetime.now()
            session.add(exp)
            session.commit()

    def _run_generation(self, name, n_frames):
        self.master.add_log(f"Старт регистрации: '{name}' ({n_frames} кадров)")

        new_data = [self.master.headers[:]]

        for i in range(1, n_frames + 1):
            row = [
                round(random.uniform(0.1, 0.9), 3),
                round(random.uniform(0.1, 0.9), 3),
                round(random.uniform(0.1, 0.9), 3),
                round(random.uniform(0.1, 0.9), 3),
                round(random.uniform(0.1, 0.9), 3),
                round(random.uniform(0.4, 0.6), 4),
                round(random.uniform(0.001, 0.005), 5),
                random.randint(10, 20),
                random.randint(40, 50),
                f"{random.uniform(68.5, 69.9):.1f}"
            ]
            new_data.append(row)

            if i % max(1, n_frames // 20) == 0:
                progress = i / n_frames
                self.progress_bar.set(progress)
                self.loading_label.configure(text=f"Генерация... {int(progress*100)}%")
                self.update_idletasks()

        self.master.set_full_data(new_data)
        self.master.add_log(f"✅ Сгенерировано {n_frames} строк")

        self.destroy()


class AboutWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("О программе")
        self.geometry("400x350")
        self.attributes("-topmost", True)
        self.grab_set()
        self.resizable(False, False)
        self.after(100, self._center_window)

        ctk.CTkLabel(self, text="📊", font=("Arial", 60)).pack(pady=(20, 10))
        ctk.CTkLabel(self, text="Система регистрации и обработки данных", 
                     font=("Arial", 18, "bold")).pack()
        desc = "Комплекс программных средств\nдля регистрации и обработки данных измерений"
        ctk.CTkLabel(self, text=desc, font=("Arial", 13), justify="center").pack(pady=20)

        info = ctk.CTkFrame(self, fg_color="transparent")
        info.pack(pady=10)
        ctk.CTkLabel(info, text="Разработчик:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, sticky="e")
        ctk.CTkLabel(info, text="Бригада №1", font=("Arial", 12)).grid(row=0, column=1, padx=5, sticky="w")

        ctk.CTkButton(self, text="Закрыть", width=100, command=self.destroy).pack(pady=(20, 10))

    def _center_window(self):
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.operator_name = "—"
        self.all_data = []
        self.current_page = 0
        self.rows_per_page = 100

        self.title("Система мониторинга")
        self.after(0, lambda: self.state('zoomed'))

        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Верхняя панель
        self.top_panel = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.top_panel.grid(row=0, column=0, sticky="nsew")

        btn_frame = ctk.CTkFrame(self.top_panel, fg_color="transparent")
        btn_frame.pack(side="left", padx=10)

        buttons = [
            ("Регистрация данных", self.open_registration_setup),
            ("Управление данными", None),
            ("Научно-технический расчет", None),
            ("О программе", self.open_about)
        ]
        for text, cmd in buttons:
            ctk.CTkButton(btn_frame, text=text, width=150, command=cmd).pack(side="left", padx=5, pady=10)

        self.operator_label = ctk.CTkLabel(self.top_panel, text=f"Оператор: {self.operator_name}", 
                                           font=("Arial", 14, "bold"))
        self.operator_label.pack(side="right", padx=20)

        # Область таблицы
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="nsew")

        self.sheet = tksheet.Sheet(
            self.table_frame,
            show_row_index=True,
            font=("Arial", 11, "normal"),
            header_font=("Arial", 12, "bold"),
            theme="dark",
            all_columns_displayed_stretched=True 
        )

        self.sheet.pack(expand=True, fill="both", padx=5, pady=5)
        self.sheet.enable_bindings("all")

        # Панель пагинации
        self.pagination_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.pagination_frame.pack(fill="x", pady=(0, 10))

        self.btn_prev = ctk.CTkButton(self.pagination_frame, text="◀ Предыдущая", width=130,
                                      command=self.prev_page, state="disabled")
        self.btn_prev.pack(side="left", padx=10)

        self.page_label = ctk.CTkLabel(self.pagination_frame, text="Страница 1 / 1", font=("Arial", 12))
        self.page_label.pack(side="left", expand=True)

        self.btn_next = ctk.CTkButton(self.pagination_frame, text="Следующая ▶", width=130,
                                      command=self.next_page, state="disabled")
        self.btn_next.pack(side="right", padx=10)

        # Журнал
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=2, column=0, padx=10, pady=(5, 20), sticky="nsew")

        log_header = ctk.CTkFrame(self.log_frame, fg_color="transparent")
        log_header.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(log_header, text="Журнал событий", font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkButton(log_header, text="Очистить", width=80, height=24,
                      fg_color="gray", hover_color="#666666",
                      command=self.clear_logs).pack(side="right")

        self.log_view = ctk.CTkTextbox(self.log_frame, font=("Courier", 12), height=10)
        self.log_view.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_view.configure(state="disabled")

        self.headers = ["Канал 1", "Канал 2", "Канал 3", "Канал 4", "Канал 5",
                        "Канал 6 Среднее", "Канал 6 Дисперсия", "Канал 19", "Канал 49", "Канал 69 F"]

        self.sheet.headers(self.headers)
        self.sheet.set_all_column_widths()
        self.sheet.redraw()
        self.ask_user_info()

    # ====================== МЕТОДЫ ======================

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_view.configure(state="normal")
        self.log_view.insert("end", f"[{timestamp}] {message}\n")
        self.log_view.see("end")
        self.log_view.configure(state="disabled")

    def clear_logs(self):
        self.log_view.configure(state="normal")
        self.log_view.delete("1.0", "end")
        self.log_view.configure(state="disabled")

    def set_full_data(self, full_data):
        self.all_data = full_data
        self.current_page = 0
        self.show_current_page()

    def auto_fit_columns(self):
        """Автоматически подгоняет ширину всех колонок под содержимое"""
        try:
            self.sheet.set_all_column_widths()   # основной метод tksheet для авто-fit
        except:
            # запасной вариант (ручной расчёт)
            for col in range(self.sheet.get_total_columns()):
                self.sheet.column_width(col, value = "text") 

    def show_current_page(self):
        if not self.all_data:
            return

        total_rows = len(self.all_data) - 1
        total_pages = max(1, (total_rows + self.rows_per_page - 1) // self.rows_per_page)

        start = 1 + self.current_page * self.rows_per_page
        end = start + self.rows_per_page
        page_data = self.all_data[start:end]

        self.sheet.set_sheet_data(page_data)

        self.page_label.configure(text=f"Страница {self.current_page + 1} / {total_pages}")

        self.btn_prev.configure(state="normal" if self.current_page > 0 else "disabled")
        self.btn_next.configure(state="normal" if self.current_page < total_pages - 1 else "disabled")

        # Авторастяжение колонок после загрузки данных
        self.after(10, self.auto_fit_columns)   # небольшая задержка для корректного рендера

        self.sheet.see(row = 0, column = 0)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def next_page(self):
        total_rows = len(self.all_data) - 1
        total_pages = max(1, (total_rows + self.rows_per_page - 1) // self.rows_per_page)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.show_current_page()

    def clear_table(self):
        self.sheet.set_sheet_data([])
        self.all_data = []
        self.current_page = 0
        self.add_log("Таблица очищена")

    def update_operator_info(self):
        self.operator_label.configure(text=f"Оператор: {self.operator_name}")
        self.add_log(f"Оператор {self.operator_name} вошел в систему")

    def open_registration_setup(self):
        RegistrationSetupWindow(self)

    def open_about(self):
        AboutWindow(self)
        self.add_log("Открыто окно 'О программе'")

    def ask_user_info(self):
        self.after(200, lambda: LoginWindow(self))