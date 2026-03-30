import time
import queue
import threading
import random


class CommentQueue:
    def __init__(self, ai_responder, tts, app):
        self.ai = ai_responder
        self.tts = tts
        self.app = app
        
        # Queue ưu tiên
        self.high_priority = queue.Queue()  # Chào MINI, câu hỏi
        self.normal_priority = queue.Queue()  # Bình thường
        
        # Delay giữa responses
        self.min_delay = 5  # giây
        self.max_delay = 8
        
        # Gộp chào
        self.greet_buffer = []
        self.greet_buffer_time = 0
        self.greet_buffer_window = 3  # 3 giây
        
        # Worker thread
        self.running = False
        self.worker_thread = None
        
    def start(self):
        """Khởi động worker thread"""
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        print("[Queue] Da khoi dong comment queue")
    
    def stop(self):
        """Dừng worker thread"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=2)
        print("[Queue] Da dung comment queue")
    
    def add_comment(self, username: str, message: str):
        """Thêm comment vào queue"""
        msg_lower = message.lower()
        
        # Phát hiện ưu tiên cao
        is_high_priority = any([
            "mini" in msg_lower,
            "?" in message,
            "hỏi" in msg_lower,
            "cho hỏi" in msg_lower,
            len(message) > 20  # Câu dài thường là câu hỏi
        ])
        
        # Phát hiện spam/lặp đơn giản
        if self._is_spam(message):
            print(f"[Queue] Bỏ spam: {username}: {message[:20]}")
            return
        
        comment = {
            'username': username,
            'message': message,
            'time': time.time()
        }
        
        if is_high_priority:
            self.high_priority.put(comment)
            print(f"[Queue] Uu tien: {username}: {message[:30]}")
        else:
            self.normal_priority.put(comment)
            print(f"[Queue] Binh thuong: {username}: {message[:30]}")
    
    def add_join(self, username: str):
        """Thêm người vào vào buffer để gộp"""
        now = time.time()
        
        # Reset buffer nếu quá lâu
        if now - self.greet_buffer_time > self.greet_buffer_window:
            self._flush_greet_buffer()
        
        self.greet_buffer.append(username)
        self.greet_buffer_time = now
    
    def _flush_greet_buffer(self):
        """Xử lý buffer chào hỏi"""
        if not self.greet_buffer:
            return
        
        if len(self.greet_buffer) == 1:
            # Chỉ 1 người → chào bình thường
            username = self.greet_buffer[0]
            greeting = self.ai.greet_viewer(username)
            self._speak(f"👋 {username} vua vao live\n🎀 MINI: {greeting}", greeting)
        else:
            # Nhiều người → gộp lại
            count = len(self.greet_buffer)
            names = ", ".join(self.greet_buffer[:3])  # Lấy 3 người đầu
            
            if count <= 3:
                greeting = f"Dạ MINI chào {names} nha, vào chơi với MINI nhe ạ!"
            else:
                greeting = f"Ôi MINI thấy {count} bạn vừa vào, chào cả nhà nha! Vào comment đi ạ 💕"
            
            self._speak(f"👋 {count} người vua vao live\n🎀 MINI: {greeting}", greeting)
        
        self.greet_buffer.clear()
        self.greet_buffer_time = 0
    
    def _is_spam(self, message: str) -> bool:
        """Phát hiện spam đơn giản"""
        # Chỉ emoji
        if all(not c.isalnum() for c in message):
            return True
        
        # Quá ngắn
        if len(message) < 2:
            return True
        
        return False
    
    def _worker(self):
        """Worker thread xử lý queue"""
        print("[Queue] Worker bat dau")
        
        while self.running:
            try:
                # Flush buffer chào trước
                now = time.time()
                if self.greet_buffer and now - self.greet_buffer_time > self.greet_buffer_window:
                    self._flush_greet_buffer()
                
                # Lấy comment từ queue (ưu tiên high trước)
                comment = None
                try:
                    comment = self.high_priority.get(timeout=0.5)
                except queue.Empty:
                    try:
                        comment = self.normal_priority.get(timeout=0.5)
                    except queue.Empty:
                        continue
                
                if comment:
                    self._process_comment(comment)
                    
                    # Delay ngẫu nhiên
                    delay = random.uniform(self.min_delay, self.max_delay)
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"[Queue] Loi worker: {e}")
                time.sleep(1)
        
        print("[Queue] Worker ket thuc")
    
    def _process_comment(self, comment: dict):
        """Xử lý 1 comment"""
        username = comment['username']
        message = comment['message']
        
        # Gọi AI
        reply = self.ai.reply(username, message)
        
        # Hiển thị và nói
        self._speak(f"👤 {username}: {message}\n🎀 MINI: {reply}", reply)
    
    def _speak(self, chat_text: str, tts_text: str):
        """Hiển thị chat và nói"""
        if self.app:
            self.app.add_chat(chat_text)
        if self.tts:
            self.tts.speak(tts_text)
