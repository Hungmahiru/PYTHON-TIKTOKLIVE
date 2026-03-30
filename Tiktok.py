import os
import sys
import time
import threading
import traceback
import warnings
import asyncio

warnings.filterwarnings("ignore", category=RuntimeWarning)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from giaodien.main_ui import MiniAIApp
from tiktok.client import TikTokClient
from ai.responder import AIResponder
from ai.auto_question import AutoQuestion
from ai.music_player import MusicPlayer
from ai.comment_queue import CommentQueue
from tts.tts_engine import TTSEngine
from vsee_face.launcher import launch_vseeface, stop_vseeface


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = None
ai = None
tts = None
auto_q = None
music = None
comment_queue = None
tiktok = None
auto_talk_thread = None
auto_talk_running = False


def cleanup():
    global auto_talk_running, comment_queue
    print("[App] Dang dong ung dung...")
    auto_talk_running = False
    
    if comment_queue:
        comment_queue.stop()
    
    if tiktok:
        tiktok.disconnect()
    
    stop_vseeface()
    print("[App] Da dong ung dung!")


def main():
    global app, ai, tts, auto_q, music, comment_queue, tiktok, auto_talk_running
    
    try:
        launch_vseeface()

        tts = TTSEngine()
        ai = AIResponder(tts=tts)
        auto_q = AutoQuestion()
        music = MusicPlayer()

        tiktok = TikTokClient()

        def on_login_handler(username):
            handle_login(username, tiktok)

        def on_logout_handler():
            tiktok.disconnect()

        app = MiniAIApp(
            on_login=on_login_handler,
            on_logout=on_logout_handler,
            on_comment=None,
            on_join=None
        )
        
        app.set_on_close(cleanup)

        # Khởi tạo queue
        comment_queue = CommentQueue(ai, tts, app)
        comment_queue.start()

        def handle_comment_callback(username, message):
            auto_q.update_activity()
            
            # Kiểm tra yêu cầu mở nhạc trước
            is_music, music_response = music.handle_request(username, message)
            if is_music:
                if app:
                    app.add_chat(f"👤 {username}: {message}\n🎀 MINI: {music_response}")
                if tts:
                    tts.speak(music_response)
                return
            
            # Đưa vào queue để xử lý
            comment_queue.add_comment(username, message)

        def handle_join_callback(username):
            # Đưa vào buffer để gộp
            comment_queue.add_join(username)

        def handle_gift_callback(username, gift_name, coins, count):
            auto_q.update_activity()
            try:
                handle_gift(username, gift_name, coins, count)
            except Exception as e:
                print(f"[Error] Gift: {e}")

        def handle_view_update(count):
            try:
                app.update_view_count(count)
            except:
                pass

        tiktok.set_callbacks(
            on_comment=handle_comment_callback,
            on_join=handle_join_callback,
            on_gift=handle_gift_callback
        )
        tiktok.on_view_update = handle_view_update

        auto_talk_running = True
        start_auto_question()

        app.run()
        
    except Exception as e:
        print(f"[Error] Main: {e}")
        traceback.print_exc()
        input("Nhan Enter de dong...")


def start_auto_question():
    global auto_talk_thread
    
    def auto_question_loop():
        while auto_talk_running:
            time.sleep(3)
            
            if auto_q:
                question = auto_q.check_and_get_question()
                if question:
                    try:
                        if app:
                            app.add_chat(f"MINI: {question}")
                        if tts:
                            tts.speak(question)
                    except Exception as e:
                        print(f"[Error] Auto question: {e}")
    
    auto_talk_thread = threading.Thread(target=auto_question_loop, daemon=True)
    auto_talk_thread.start()


def handle_login(username, tiktok):
    tiktok.connect(username)
    if app:
        app.add_chat(f"Da ket noi live: {username}")
    
    if auto_q and tts:
        opening = auto_q.get_opening_script()
        if app:
            app.add_chat(f"MINI: {opening}")
        tts.speak(opening)
        auto_q.update_activity()


def handle_join(username):
    if app:
        app.add_chat(f"{username} vua vao live")
    
    if ai and tts:
        greeting = ai.greet_viewer(username)
        if app:
            app.add_chat(f"MINI: {greeting}")
        tts.speak(greeting)


def handle_comment(username, message):
    if app:
        app.add_chat(f"{username}: {message}")

    # Kiểm tra yêu cầu mở nhạc
    if music:
        is_music, music_response = music.handle_request(username, message)
        if is_music:
            if app:
                app.add_chat(f"MINI: {music_response}")
            if tts:
                tts.speak(music_response)
            return

    # Trả lời bình thường
    if ai:
        reply = ai.reply(username, message)
        if app:
            app.add_chat(f"MINI: {reply}")
        if tts:
            tts.speak(reply)


def handle_gift(username, gift_name, coins, count):
    total_coins = coins * count
    
    if app:
        app.add_chat(f"GIFT: {username} tang {count}x {gift_name} ({total_coins} xu)")
    
    # Cấp 1 lượt mở nhạc cho người tặng quà (1 quà = 1 bài)
    if music:
        music.add_song_credit(username, 1)
    
    if ai and tts:
        thank_msg = ai.thank_gift(username, gift_name, count, total_coins)
        if app:
            app.add_chat(f"MINI: {thank_msg}")
        tts.speak(thank_msg)


if __name__ == "__main__":
    main()
