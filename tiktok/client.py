import threading
import time
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, DisconnectEvent, CommentEvent, GiftEvent, JoinEvent


class TikTokClient:
    def __init__(self):
        self.username = None
        self.connected = False
        self.client = None
        self.thread = None
        self.on_comment = None
        self.on_join = None
        self.on_gift = None
        self.on_view_update = None
        self.should_run = False
        
        # Tránh lặp lại
        self.recent_comments = []  # [(user, message, time), ...]
        self.recent_joins = []     # [(user, time), ...]
        self.max_recent = 50
        self.duplicate_window = 30  # 30 giây - tránh lặp

    def connect(self, username: str):
        self.username = username.replace("@", "").strip()
        self.should_run = True
        print(f"[TikTok] Dang ket noi toi: {self.username}")
        
        def run_client():
            while self.should_run:
                try:
                    self.client = TikTokLiveClient(unique_id=self.username)
                    self._setup_events()
                    self.client.run()
                except Exception as e:
                    error_msg = str(e)
                    if "pending" not in error_msg.lower():
                        print(f"[TikTok] Loi: {error_msg[:80]}")
                    self.connected = False
                    
                if self.should_run:
                    print("[TikTok] Mat ket noi, thu lai sau 3 giay...")
                    time.sleep(3)

        self.thread = threading.Thread(target=run_client, daemon=True)
        self.thread.start()

    def _is_duplicate_comment(self, user: str, message: str) -> bool:
        """Kiểm tra comment trùng lặp"""
        now = time.time()
        
        # Xóa comment cũ
        self.recent_comments = [
            (u, m, t) for u, m, t in self.recent_comments 
            if now - t < self.duplicate_window
        ]
        
        # Kiểm tra trùng
        for u, m, t in self.recent_comments:
            if u == user and m == message:
                return True
        
        # Thêm mới
        self.recent_comments.append((user, message, now))
        if len(self.recent_comments) > self.max_recent:
            self.recent_comments.pop(0)
        
        return False

    def _is_duplicate_join(self, user: str) -> bool:
        """Kiểm tra join trùng lặp"""
        now = time.time()
        
        # Xóa join cũ
        self.recent_joins = [
            (u, t) for u, t in self.recent_joins 
            if now - t < self.duplicate_window
        ]
        
        # Kiểm tra trùng
        for u, t in self.recent_joins:
            if u == user:
                return True
        
        # Thêm mới
        self.recent_joins.append((user, now))
        if len(self.recent_joins) > self.max_recent:
            self.recent_joins.pop(0)
        
        return False

    def _setup_events(self):
        @self.client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            self.connected = True
            print(f"[TikTok] Da ket noi thanh cong!")

        @self.client.on(DisconnectEvent)
        async def on_disconnect(event: DisconnectEvent):
            self.connected = False

        @self.client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            try:
                if self.on_comment:
                    user = event.user.nickname or event.user.unique_id
                    message = event.comment
                    
                    # Bỏ qua nếu trùng
                    if self._is_duplicate_comment(user, message):
                        return
                    
                    self.on_comment(user, message)
            except:
                pass

        @self.client.on(JoinEvent)
        async def on_join(event: JoinEvent):
            try:
                if self.on_join:
                    user = event.user.nickname or event.user.unique_id
                    
                    # Bỏ qua nếu trùng
                    if self._is_duplicate_join(user):
                        return
                    
                    self.on_join(user)
            except:
                pass

        @self.client.on(GiftEvent)
        async def on_gift(event: GiftEvent):
            try:
                if self.on_gift and event.gift:
                    user = event.user.nickname or event.user.unique_id
                    gift_name = event.gift.name or "Qua"
                    coins = event.gift.diamond_count or 0
                    count = event.repeat_count or 1
                    if event.gift.streakable and event.streaking:
                        return
                    self.on_gift(user, gift_name, coins, count)
            except:
                pass

    def disconnect(self):
        self.should_run = False
        self.connected = False
        if self.client:
            try:
                self.client.stop()
            except:
                pass
        print("[TikTok] Da ngat ket noi")

    def set_callbacks(self, on_comment=None, on_join=None, on_gift=None):
        self.on_comment = on_comment
        self.on_join = on_join
        self.on_gift = on_gift
