import threading
import os
import time
import queue

_audio_queue = queue.Queue()
_player_thread = None
_running = False


def _player_worker():
    global _running
    import pygame
    
    while _running:
        try:
            path = _audio_queue.get(timeout=1)
            if path is None:
                continue
                
            if not os.path.exists(path):
                continue
            
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.quit()
                
                time.sleep(0.1)
                
                try:
                    os.remove(path)
                except:
                    pass
                    
            except Exception as e:
                print(f"[Audio] Loi: {str(e)[:30]}")
                try:
                    pygame.mixer.quit()
                except:
                    pass
                    
        except queue.Empty:
            continue
        except Exception as e:
            print(f"[Audio] Worker error: {str(e)[:30]}")


def start_player():
    global _player_thread, _running
    if _player_thread is None or not _player_thread.is_alive():
        _running = True
        _player_thread = threading.Thread(target=_player_worker, daemon=True)
        _player_thread.start()


def play_audio(path: str):
    global _running
    if not _running:
        start_player()
    _audio_queue.put(path)


def stop_player():
    global _running
    _running = False
