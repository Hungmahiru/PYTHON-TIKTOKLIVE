import customtkinter as ctk


class LiveView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=("#2a2a3e", "#1a1a2e"), corner_radius=15)

        self.view_count = 0

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=20)

        title_label = ctk.CTkLabel(
            header_frame,
            text="📺 Live Stream",
            font=ctk.CTkFont(size=28, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left")

        stats_frame = ctk.CTkFrame(header_frame, fg_color=("#3a3a4e", "#2a2a3e"), corner_radius=12)
        stats_frame.pack(side="right", padx=10)

        self.view_label = ctk.CTkLabel(
            stats_frame,
            text="👁️ 0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#4a90e2", "#5ba3f5")
        )
        self.view_label.pack(padx=20, pady=12)

        chat_container = ctk.CTkFrame(self, fg_color=("#1a1a2e", "#0f0f1e"), corner_radius=12)
        chat_container.pack(expand=True, fill="both", padx=25, pady=(0, 25))

        chat_header = ctk.CTkFrame(chat_container, fg_color="transparent")
        chat_header.pack(fill="x", padx=20, pady=15)

        chat_title = ctk.CTkLabel(
            chat_header,
            text="💬 Chat Live",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        chat_title.pack(side="left")

        self.chat_box = ctk.CTkTextbox(
            chat_container,
            state="disabled",
            font=ctk.CTkFont(size=14),
            wrap="word",
            fg_color=("#0f0f1e", "#050508"),
            text_color=("#ffffff", "#ffffff"),
            corner_radius=10
        )
        self.chat_box.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    def add_message(self, text):
        self.chat_box.configure(state="normal")

        if "MINI:" in text:
            color = "#ff6b9d"
            formatted = f"🎀 {text}\n"
            self.chat_box.insert("end", formatted, "mini_message")
            self.chat_box.tag_config("mini_message", foreground=color)
        elif "GIFT:" in text:
            color = "#f59e0b"
            formatted = f"🎁 {text.replace('GIFT:', '').strip()}\n"
            self.chat_box.insert("end", formatted, "gift_message")
            self.chat_box.tag_config("gift_message", foreground=color)
        elif "vua vao live" in text or "vào live" in text:
            color = "#4ade80"
            formatted = f"👋 {text}\n"
            self.chat_box.insert("end", formatted, "join_message")
            self.chat_box.tag_config("join_message", foreground=color)
        elif "Da ket noi" in text or "Đã kết nối" in text:
            color = "#4ade80"
            formatted = f"✅ {text}\n"
            self.chat_box.insert("end", formatted, "system_message")
            self.chat_box.tag_config("system_message", foreground=color)
        elif ":" in text:
            parts = text.split(":", 1)
            if len(parts) == 2:
                username = parts[0].strip()
                message = parts[1].strip()
                color = "#fbbf24"
                formatted = f"👤 {username}: {message}\n"
                self.chat_box.insert("end", formatted, "user_message")
                self.chat_box.tag_config("user_message", foreground=color)
            else:
                self.chat_box.insert("end", f"{text}\n")
        else:
            self.chat_box.insert("end", f"{text}\n")

        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    def update_view(self, count):
        self.view_count = count
        formatted_count = f"{count:,}".replace(",", ".")
        self.view_label.configure(text=f"👁️ {formatted_count}")
