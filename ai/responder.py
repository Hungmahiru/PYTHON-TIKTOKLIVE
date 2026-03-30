import os
import json
import random
import requests
import subprocess
import time
import atexit


class AIResponder:
    def __init__(self, tts=None):
        self.tts = tts
        self.config = self.load_config()
        self.model = self.config.get("model", "qwen2.5:32b")
        self.ollama_url = "http://localhost:11434/api/generate"
        self.connected = False
        self.ollama_process = None
        
        # Tránh lặp câu trả lời
        self.recent_responses = []
        self.max_recent_responses = 10
        
        self._start_ollama()
        self._test_connection()
        atexit.register(self._stop_ollama)

    def _start_ollama(self):
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=3)
            if response.status_code == 200:
                print("[AI] Ollama da chay san")
                return
        except:
            pass
        
        print("[AI] Dang khoi dong Ollama...")
        try:
            env = os.environ.copy()
            env["CUDA_VISIBLE_DEVICES"] = "1"
            self.ollama_process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
                env=env
            )
            time.sleep(10)
            print("[AI] Ollama da khoi dong (GPU 1)")
        except Exception as e:
            print(f"[AI] Loi khoi dong: {str(e)[:50]}")

    def _stop_ollama(self):
        try:
            subprocess.run(["taskkill", "/F", "/IM", "ollama.exe"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["taskkill", "/F", "/IM", "ollama_llama_server.exe"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass

    def _test_connection(self):
        for attempt in range(3):
            try:
                print(f"[AI] Test ket noi Ollama lan {attempt+1}...")
                response = requests.post(
                    self.ollama_url,
                    json={"model": self.model, "prompt": "Hi", "stream": False},
                    timeout=120
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get("response", ""):
                        self.connected = True
                        print(f"[AI] Ket noi OK - Model: {self.model}")
                        if self.tts:
                            self.tts.speak("Dạ MINI sẵn sàng rồi ạ")
                        return
            except Exception as e:
                print(f"[AI] Loi lan {attempt+1}: {str(e)[:40]}")
            time.sleep(5)
        
        print("[AI] KHONG KET NOI DUOC OLLAMA!")
        self.connected = False

    def load_config(self):
        config_path = os.path.join("config", "ai.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"model": "qwen2.5:32b"}

    def _get_unique_response(self, options: list) -> str:
        """Lấy câu trả lời không trùng"""
        available = [opt for opt in options if opt not in self.recent_responses]
        if not available:
            self.recent_responses.clear()
            available = options
        response = random.choice(available)
        self.recent_responses.append(response)
        if len(self.recent_responses) > self.max_recent_responses:
            self.recent_responses.pop(0)
        return response

    def _call_ollama(self, prompt: str) -> str:
        """Gọi Ollama"""
        if not self.connected:
            return None
            
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 60}
                },
                timeout=30
            )
            if response.status_code == 200:
                result = response.json().get("response", "").strip()
                result = result.split('\n')[0].strip('"\'')
                return result if len(result) > 5 else None
        except Exception as e:
            print(f"[AI] Loi Ollama: {str(e)[:30]}")
        return None

    def reply(self, username: str, message: str) -> str:
        """Trả lời bình luận"""
        prompt = f'Bạn là MINI - AI livestream TikTok. Người xem "{username}" nói: "{message}". Trả lời ngắn 1 câu, gọi tên {username}, có dạ ạ, đầy đủ dấu tiếng Việt.'
        
        result = self._call_ollama(prompt)
        if result:
            if username.lower() not in result.lower():
                result = f"Dạ {username} ơi, {result}"
            return result
        
        return self._fallback_reply(username, message)

    def _fallback_reply(self, username: str, message: str) -> str:
        msg = message.lower()
        
        if any(w in msg for w in ["hi", "hello", "chào", "chao"]):
            options = [
                f"Dạ chào {username} nha, rất vui được gặp bạn ạ!",
                f"Dạ hi {username} nha, bạn khỏe không ạ?",
                f"Chào {username} nha, có gì vui kể MINI nghe ạ!"
            ]
            return self._get_unique_response(options)
        
        if any(w in msg for w in ["xinh", "đẹp", "cute"]):
            options = [
                f"Dạ cảm ơn {username} khen MINI nha!",
                f"Ôi {username} khen vui quá ạ!",
                f"Dạ {username} cũng xinh lắm ạ!"
            ]
            return self._get_unique_response(options)
        
        options = [
            f"Dạ {username} ơi, cảm ơn bạn đã chia sẻ nha!",
            f"Ồ vậy hả {username}, hay quá ạ!",
            f"Dạ {username} nói hay đó ạ!"
        ]
        return self._get_unique_response(options)

    def greet_viewer(self, username: str) -> str:
        """Chào người mới"""
        prompt = f'Bạn là MINI - AI livestream TikTok. Người mới "{username}" vào live. Chào họ ngắn 1 câu, gọi tên {username}, có dạ ạ, kêu ở lại, đầy đủ dấu tiếng Việt.'
        
        result = self._call_ollama(prompt)
        if result:
            if username.lower() not in result.lower():
                result = f"Dạ chào {username} nha, {result}"
            return result
        
        options = [
            f"Dạ chào {username} nha, vào chơi với MINI đi!",
            f"Ồ {username} vào nè, ngồi chơi nha!",
            f"Chào {username}, comment cho MINI biết bạn ạ!"
        ]
        return self._get_unique_response(options)

    def thank_gift(self, username: str, gift_name: str, count: int, total_coins: int) -> str:
        """Cảm ơn quà"""
        prompt = f'Bạn là MINI - AI livestream TikTok. "{username}" tặng {count}x {gift_name} ({total_coins} xu). Cảm ơn ngắn 1 câu, gọi tên {username}, có dạ ạ, xúc động, đầy đủ dấu tiếng Việt.'
        
        result = self._call_ollama(prompt)
        if result:
            if username.lower() not in result.lower():
                result = f"Dạ {username} ơi, {result}"
            return result
        
        if total_coins >= 500:
            options = [f"Dạ trời ơi {username} ơi, cảm ơn bạn nhiều lắm ạ! 🎁"]
        else:
            options = [f"Dạ cảm ơn {username} tặng {gift_name} nha ạ!"]
        return self._get_unique_response(options)
