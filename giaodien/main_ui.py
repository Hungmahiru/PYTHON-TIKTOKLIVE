import os
import json
import customtkinter as ctk
from giaodien.live_view import LiveView
from giaodien.settings_ui import SettingsView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SESSION_FILE = os.path.join("config", "session.json")


class MiniAIApp:
    def __init__(self, on_login, on_logout=None, on_comment=None, on_join=None):
        self.on_login = on_login
        self.on_logout_callback = on_logout
        self.on_comment = on_comment
        self.on_join = on_join
        self.current_page = "home"
        self.logged_username = ""
        self.chat_history = []
        self.view_count = 0

        self.app = ctk.CTk()
        self.app.title("MINI AI - TikTok Live Assistant")
        self.app.geometry("1200x700")
        self.app.configure(fg_color=("#1a1a2e", "#0f0f1e"))

        saved_username = self.load_session()
        if saved_username:
            self.logged_username = saved_username
            self.on_login(saved_username)
            self.show_main()
        else:
            self.show_login()

    def load_session(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("username", "")
            except:
                pass
        return ""

    def save_session(self, username):
        os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump({"username": username}, f, ensure_ascii=False)

    def delete_session(self):
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

    def show_login(self):
        self.clear()

        main_container = ctk.CTkFrame(self.app, fg_color="transparent")
        main_container.pack(expand=True, fill="both")

        left_panel = ctk.CTkFrame(main_container, fg_color="transparent", width=400)
        left_panel.pack(side="left", expand=True, fill="both", padx=50, pady=50)

        logo_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        logo_frame.pack(expand=True, fill="both")

        title_label = ctk.CTkLabel(
            logo_frame,
            text="MINI AI",
            font=ctk.CTkFont(size=56, weight="bold"),
            text_color=("#4a90e2", "#5ba3f5")
        )
        title_label.pack(pady=(0, 10))

        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="TikTok Live Assistant",
            font=ctk.CTkFont(size=20),
            text_color=("#888888", "#aaaaaa")
        )
        subtitle_label.pack(pady=(0, 60))

        form_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        form_frame.pack(fill="x", pady=20)

        username_label = ctk.CTkLabel(
            form_frame,
            text="TikTok Username",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        username_label.pack(fill="x", pady=(0, 8))

        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Nhập username TikTok Live",
            height=50,
            font=ctk.CTkFont(size=16),
            corner_radius=12
        )
        self.username_entry.pack(fill="x", pady=(0, 20))
        self.username_entry.bind("<Return>", lambda e: self.login())

        self.connect_button = ctk.CTkButton(
            form_frame,
            text="🚀 Kết nối Live",
            command=self.login,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=12,
            fg_color=("#4a90e2", "#5ba3f5"),
            hover_color=("#357abd", "#4a90e2")
        )
        self.connect_button.pack(fill="x", pady=(0, 10))

        info_label = ctk.CTkLabel(
            form_frame,
            text="Nhập username TikTok để bắt đầu live stream",
            font=ctk.CTkFont(size=12),
            text_color=("#666666", "#999999")
        )
        info_label.pack()

        right_panel = ctk.CTkFrame(main_container, fg_color=("#2a2a3e", "#1a1a2e"), width=500)
        right_panel.pack(side="right", expand=True, fill="both", padx=(0, 50), pady=50)

        feature_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        feature_frame.pack(expand=True, fill="both", padx=40, pady=40)

        features = [
            ("🤖", "AI Trả lời tự động", "Hệ thống AI thông minh trả lời comment"),
            ("🎤", "Text-to-Speech", "Chuyển đổi văn bản thành giọng nói"),
            ("👤", "Avatar ảo VSeeFace", "Avatar nhép miệng theo giọng nói"),
            ("💬", "Quản lý chat", "Theo dõi và xử lý comment realtime")
        ]

        for icon, title, desc in features:
            feature_item = ctk.CTkFrame(feature_frame, fg_color=("#3a3a4e", "#2a2a3e"), corner_radius=15)
            feature_item.pack(fill="x", pady=15)

            icon_label = ctk.CTkLabel(
                feature_item,
                text=icon,
                font=ctk.CTkFont(size=32)
            )
            icon_label.pack(side="left", padx=20, pady=15)

            text_frame = ctk.CTkFrame(feature_item, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=15)

            title_label = ctk.CTkLabel(
                text_frame,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            title_label.pack(anchor="w", pady=(0, 5))

            desc_label = ctk.CTkLabel(
                text_frame,
                text=desc,
                font=ctk.CTkFont(size=12),
                text_color=("#888888", "#aaaaaa"),
                anchor="w"
            )
            desc_label.pack(anchor="w")

    def login(self):
        username = self.username_entry.get().strip()
        if not username:
            return

        self.logged_username = username
        self.save_session(username)
        self.on_login(username)
        self.show_main()

    def logout(self):
        self.delete_session()
        self.logged_username = ""
        if self.on_logout_callback:
            self.on_logout_callback()
        self.show_login()

    def show_main(self):
        self.clear()

        self.sidebar = ctk.CTkFrame(
            self.app,
            width=220,
            fg_color=("#2a2a3e", "#1a1a2e"),
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        logo_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_container.pack(fill="x", padx=20, pady=30)

        logo_label = ctk.CTkLabel(
            logo_container,
            text="MINI AI",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#4a90e2", "#5ba3f5")
        )
        logo_label.pack()

        subtitle_label = ctk.CTkLabel(
            logo_container,
            text="Live Assistant",
            font=ctk.CTkFont(size=12),
            text_color=("#888888", "#aaaaaa")
        )
        subtitle_label.pack(pady=(5, 0))

        account_frame = ctk.CTkFrame(self.sidebar, fg_color=("#3a3a4e", "#2a2a3e"), corner_radius=10)
        account_frame.pack(fill="x", padx=15, pady=(20, 0))

        account_icon = ctk.CTkLabel(
            account_frame,
            text="👤",
            font=ctk.CTkFont(size=20)
        )
        account_icon.pack(side="left", padx=(15, 10), pady=12)

        account_info = ctk.CTkFrame(account_frame, fg_color="transparent")
        account_info.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=12)

        account_label = ctk.CTkLabel(
            account_info,
            text="Đang live",
            font=ctk.CTkFont(size=10),
            text_color=("#888888", "#aaaaaa"),
            anchor="w"
        )
        account_label.pack(anchor="w")

        username_label = ctk.CTkLabel(
            account_info,
            text=f"@{self.logged_username}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#4a90e2", "#5ba3f5"),
            anchor="w"
        )
        username_label.pack(anchor="w")

        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=15, pady=20)

        self.home_button = ctk.CTkButton(
            nav_frame,
            text="🏠 Trang chủ",
            command=self.show_home,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=10,
            fg_color=("#4a90e2", "#5ba3f5") if self.current_page == "home" else ("#3a3a4e", "#2a2a3e"),
            hover_color=("#357abd", "#4a90e2"),
            anchor="w"
        )
        self.home_button.pack(fill="x", pady=8)

        self.settings_button = ctk.CTkButton(
            nav_frame,
            text="⚙️ Cài đặt",
            command=self.show_settings,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=10,
            fg_color=("#4a90e2", "#5ba3f5") if self.current_page == "settings" else ("#3a3a4e", "#2a2a3e"),
            hover_color=("#357abd", "#4a90e2"),
            anchor="w"
        )
        self.settings_button.pack(fill="x", pady=8)

        self.content = ctk.CTkFrame(
            self.app,
            fg_color=("#1a1a2e", "#0f0f1e"),
            corner_radius=0
        )
        self.content.pack(side="right", expand=True, fill="both")

        self.show_home()

    def show_home(self):
        self.current_page = "home"
        self.update_nav_buttons()
        self.clear_content()
        self.live_view = LiveView(self.content)
        self.live_view.pack(expand=True, fill="both", padx=20, pady=20)
        
        for msg in self.chat_history:
            self.live_view.add_message(msg)
        self.live_view.update_view(self.view_count)

    def show_settings(self):
        self.current_page = "settings"
        self.update_nav_buttons()
        self.clear_content()
        SettingsView(self.content, on_logout=self.logout).pack(expand=True, fill="both", padx=20, pady=20)

    def update_nav_buttons(self):
        if hasattr(self, "home_button"):
            self.home_button.configure(
                fg_color=("#4a90e2", "#5ba3f5") if self.current_page == "home" else ("#3a3a4e", "#2a2a3e")
            )
        if hasattr(self, "settings_button"):
            self.settings_button.configure(
                fg_color=("#4a90e2", "#5ba3f5") if self.current_page == "settings" else ("#3a3a4e", "#2a2a3e")
            )

    def add_chat(self, text):
        self.chat_history.append(text)
        if hasattr(self, "live_view"):
            self.app.after(0, lambda: self.live_view.add_message(text))

    def update_view_count(self, count):
        self.view_count = count
        if hasattr(self, "live_view"):
            self.app.after(0, lambda: self.live_view.update_view(count))

    def clear(self):
        for w in self.app.winfo_children():
            w.destroy()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def set_on_close(self, callback):
        self.on_close_callback = callback

    def on_closing(self):
        if hasattr(self, 'on_close_callback') and self.on_close_callback:
            self.on_close_callback()
        self.app.destroy()

    def run(self):
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.mainloop()
