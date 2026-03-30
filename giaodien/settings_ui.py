import customtkinter as ctk
import json
import os


class SettingsView(ctk.CTkFrame):
    def __init__(self, master, on_logout=None):
        super().__init__(master, fg_color=("#2a2a3e", "#1a1a2e"), corner_radius=15)
        self.on_logout = on_logout

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=30)

        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ Cài đặt hệ thống",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Quản lý cấu hình và tùy chọn",
            font=ctk.CTkFont(size=14),
            text_color=("#888888", "#aaaaaa")
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))

        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=30, pady=(0, 30))

        gemini_frame = ctk.CTkFrame(
            content_frame,
            fg_color=("#3a3a4e", "#2a2a3e"),
            corner_radius=15
        )
        gemini_frame.pack(fill="x", pady=(0, 20))

        gemini_header = ctk.CTkFrame(gemini_frame, fg_color="transparent")
        gemini_header.pack(fill="x", padx=25, pady=(25, 15))

        gemini_icon = ctk.CTkLabel(
            gemini_header,
            text="🤖",
            font=ctk.CTkFont(size=24)
        )
        gemini_icon.pack(side="left")

        gemini_title = ctk.CTkLabel(
            gemini_header,
            text="API Gemini",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        gemini_title.pack(side="left", padx=(10, 0))

        gemini_desc = ctk.CTkLabel(
            gemini_frame,
            text="Nhập API Key của Google Gemini để sử dụng AI trả lời câu hỏi",
            font=ctk.CTkFont(size=12),
            text_color=("#888888", "#aaaaaa")
        )
        gemini_desc.pack(anchor="w", padx=25, pady=(0, 15))

        api_input_frame = ctk.CTkFrame(gemini_frame, fg_color="transparent")
        api_input_frame.pack(fill="x", padx=25, pady=(0, 25))

        self.api_entry = ctk.CTkEntry(
            api_input_frame,
            placeholder_text="Nhập Gemini API Key...",
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.api_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        save_api_btn = ctk.CTkButton(
            api_input_frame,
            text="💾 Lưu",
            command=self.save_api_key,
            height=45,
            width=100,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10,
            fg_color=("#4a90e2", "#5ba3f5"),
            hover_color=("#357abd", "#4a90e2")
        )
        save_api_btn.pack(side="right")

        self.load_api_key()

        logout_frame = ctk.CTkFrame(
            content_frame,
            fg_color=("#3a3a4e", "#2a2a3e"),
            corner_radius=15
        )
        logout_frame.pack(fill="x", pady=(0, 20))

        logout_header = ctk.CTkFrame(logout_frame, fg_color="transparent")
        logout_header.pack(fill="x", padx=25, pady=25)

        logout_icon = ctk.CTkLabel(
            logout_header,
            text="🚪",
            font=ctk.CTkFont(size=24)
        )
        logout_icon.pack(side="left")

        logout_info = ctk.CTkFrame(logout_header, fg_color="transparent")
        logout_info.pack(side="left", fill="x", expand=True, padx=(10, 0))

        logout_title = ctk.CTkLabel(
            logout_info,
            text="Đăng xuất",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        logout_title.pack(anchor="w")

        logout_desc = ctk.CTkLabel(
            logout_info,
            text="Đăng xuất khỏi tài khoản TikTok hiện tại",
            font=ctk.CTkFont(size=12),
            text_color=("#888888", "#aaaaaa"),
            anchor="w"
        )
        logout_desc.pack(anchor="w")

        logout_btn = ctk.CTkButton(
            logout_header,
            text="Đăng xuất",
            command=self.logout,
            height=40,
            width=120,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10,
            fg_color=("#e74c3c", "#c0392b"),
            hover_color=("#c0392b", "#a93226")
        )
        logout_btn.pack(side="right")

    def load_api_key(self):
        config_path = os.path.join("config", "ai.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                api_key = config.get("gemini_api_key", "")
                if api_key:
                    self.api_entry.insert(0, api_key)

    def save_api_key(self):
        config_path = os.path.join("config", "ai.json")
        config = {}
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        
        config["gemini_api_key"] = self.api_entry.get().strip()
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def logout(self):
        if self.on_logout:
            self.on_logout()
