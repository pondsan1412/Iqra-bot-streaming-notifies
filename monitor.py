import ctypes
import time

def toggle_monitor():
    try:
        # ปิดการเชื่อมต่อจอภาพ
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)  # SC_MONITORPOWER = 2
        # รอ 10 วินาที
        time.sleep(10)
        # เปิดการเชื่อมต่อจอภาพ
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)  # SC_MONITORPOWER = -1
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    toggle_monitor()
