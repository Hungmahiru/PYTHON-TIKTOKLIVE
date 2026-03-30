import os
import json
import asyncio
import edge_tts
import threading
import queue
from datetime import datetime
from vsee_face.audio_player import play_audio

_tts_queue = queue.Queue()
_tts_thread = None
_running = False


def _tts_worker():
    global _running
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    while _running:
        try:
            data = _tts_queue.get(timeout=1)
            if data is None:
                continue
            
            text, voice, speed, pitch, output_dir = data
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"reply_{timestamp}.mp3"
            filepath = os.path.join(output_dir, filename)
            
            rate = f"+{int((speed - 1) * 100)}%"
            pitch_str = f"+{pitch}Hz"
            
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch_str)
            loop.run_until_complete(communicate.save(filepath))
            
            if os.path.exists(filepath):
                play_audio(filepath)
                print(f"[TTS] Da noi: {text[:40]}...")
                
        except queue.Empty:
            continue
        except Exception as e:
            print(f"[TTS] Loi: {str(e)[:50]}")


class TTSEngine:
    def __init__(self):
        global _tts_thread, _running
        
        self.config = self.load_config()
        self.voice = self.config.get("voice", "vi-VN-HoaiMyNeural")
        self.speed = self.config.get("speed", 1.0)
        self.pitch = self.config.get("pitch", 10)
        self.output_dir = os.path.join("mp3", "replies")
        os.makedirs(self.output_dir, exist_ok=True)
        
        if not _running:
            _running = True
            _tts_thread = threading.Thread(target=_tts_worker, daemon=True)
            _tts_thread.start()
        
        print("[TTS] TTSEngine khoi tao")

    def load_config(self):
        config_path = os.path.join("config", "tts.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"voice": "vi-VN-HoaiMyNeural", "speed": 1.0, "pitch": 10}

    def speak(self, text: str):
        if not text or not text.strip():
            return
        _tts_queue.put((text, self.voice, self.speed, self.pitch, self.output_dir))
