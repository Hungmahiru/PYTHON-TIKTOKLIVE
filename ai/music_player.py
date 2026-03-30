import webbrowser
import urllib.parse
import atexit


class MusicPlayer:
    def __init__(self):
        self.keywords = [
            "tim bai", "tìm bài", "mở bài", "mo bai",
            "phát bài", "phat bai", "nghe bài", "nghe bai",
            "hát", "hat", "nhạc", "nhac", "bài hát", "bai hat",
            "remix", "cover", "acoustic", "beat"
        ]
        self.driver = None
        self.current_url = None
        self.song_credits = {}  # username -> số lượt mở nhạc còn lại
        self._init_driver()
        atexit.register(self.cleanup)
    
    def add_song_credit(self, username: str, count: int = 1):
        """Thêm lượt mở nhạc khi tặng quà (1 quà = 1 bài)"""
        username_lower = username.lower()
        if username_lower in self.song_credits:
            self.song_credits[username_lower] += count
        else:
            self.song_credits[username_lower] = count
        print(f"[Music] {username} co {self.song_credits[username_lower]} luot mo nhac")
    
    def use_song_credit(self, username: str) -> bool:
        """Sử dụng 1 lượt mở nhạc, trả về True nếu còn lượt"""
        username_lower = username.lower()
        if username_lower in self.song_credits and self.song_credits[username_lower] > 0:
            self.song_credits[username_lower] -= 1
            return True
        return False
    
    def get_credits(self, username: str) -> int:
        """Lấy số lượt còn lại"""
        return self.song_credits.get(username.lower(), 0)
    
    def _init_driver(self):
        """Khởi tạo Selenium WebDriver"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            
            chrome_options = Options()
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("[Music] Da khoi tao Chrome WebDriver")
        except Exception as e:
            print(f"[Music] Khong khoi tao duoc WebDriver: {str(e)[:50]}")
            self.driver = None
    
    def cleanup(self):
        if self.driver:
            try:
                self.driver.quit()
                print("[Music] Da dong WebDriver")
            except:
                pass
    
    def detect_music_request(self, message: str) -> bool:
        message_lower = message.lower()
        for keyword in self.keywords:
            if keyword in message_lower:
                return True
        return False
    
    def extract_song_name(self, message: str) -> str:
        message_lower = message.lower()
        for keyword in self.keywords:
            message_lower = message_lower.replace(keyword, "")
        remove_words = ["cho", "xin", "được", "duoc", "không", "khong", "nha", "đi", "di", "với", "voi", "toi", "tôi", "mini", "oi", "ơi"]
        for word in remove_words:
            message_lower = message_lower.replace(word, "")
        song_name = " ".join(message_lower.split()).strip()
        return song_name if song_name else message
    
    def play_on_youtube(self, song_name: str) -> str:
        try:
            from youtube_search import YoutubeSearch
            
            print(f"[Music] Dang tim: {song_name}")
            results = YoutubeSearch(song_name, max_results=1).to_dict()
            
            if results and len(results) > 0:
                video_id = results[0]['id']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                video_title = results[0]['title']
                
                if self.driver:
                    try:
                        self.driver.get(video_url)
                        self.current_url = video_url
                        return f"Dạ MINI đã mở bài '{video_title}' cho bạn rồi ạ 🎵"
                    except:
                        webbrowser.open(video_url)
                        return f"Dạ MINI đã mở bài '{video_title}' cho bạn rồi ạ 🎵"
                else:
                    webbrowser.open(video_url)
                    return f"Dạ MINI đã mở bài '{video_title}' cho bạn rồi ạ 🎵"
            else:
                query = urllib.parse.quote(song_name)
                youtube_url = f"https://www.youtube.com/results?search_query={query}"
                if self.driver:
                    self.driver.get(youtube_url)
                else:
                    webbrowser.open(youtube_url)
                return f"Dạ MINI đã tìm bài '{song_name}' cho bạn rồi ạ 🎵"
            
        except Exception as e:
            print(f"[Music] Loi: {e}")
            return "Dạ xin lỗi, MINI không mở được YouTube lúc này ạ"
    
    def handle_request(self, username: str, message: str) -> tuple:
        """
        1 QUÀ = 1 BÀI
        """
        if self.detect_music_request(message):
            song_name = self.extract_song_name(message)
            credits = self.get_credits(username)
            
            # Hết lượt hoặc chưa tặng quà
            if credits <= 0:
                import random
                soft_replies = [
                    f"Dạ {username} ơi, bài đó hay lắm nè 🎵\nBạn đợi MINI xíu nha, MINI ưu tiên comment trước ạ 💕",
                    f"Dạ {username} ơi, bài đó nhiều người thích lắm đó 🎶\nMINI note lại nhé, MINI sẽ mở nhạc cho bạn sau nha ạ",
                    f"Ui {username} thích bài đó à 🎵\nMINI đang bận trả lời mọi người, đợi xíu nha ạ"
                ]
                response = random.choice(soft_replies)
                return (True, response)
            
            # Còn lượt → Mở nhạc và trừ lượt
            if self.use_song_credit(username):
                response = self.play_on_youtube(song_name)
                remaining = self.get_credits(username)
                if remaining > 0:
                    response += f" (còn {remaining} lượt)"
                return (True, response)
        
        return (False, None)
