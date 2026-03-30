import os
import subprocess

vseeface_process = None


def launch_vseeface():
    global vseeface_process
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vseeface_path = os.path.join(base_dir, "VSeeFace", "VSeeFace.exe")
    
    if os.path.exists(vseeface_path):
        try:
            vseeface_process = subprocess.Popen(
                [vseeface_path],
                cwd=os.path.dirname(vseeface_path)
            )
            print("[VSeeFace] Da khoi dong VSeeFace!")
        except Exception as e:
            print(f"[VSeeFace] Loi khoi dong: {str(e)[:50]}")
    else:
        print(f"[VSeeFace] Khong tim thay file: {vseeface_path}")


def stop_vseeface():
    global vseeface_process
    print("[VSeeFace] Dang dung VSeeFace...")
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", "VSeeFace.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        print("[VSeeFace] Da dung VSeeFace")
    except:
        pass
