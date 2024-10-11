import sys
import keyboard
import win32gui
import win32con
import win32com.client
import io
import pythoncom
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import time

# 替换为
if sys.stdout is not None and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
else:
    print("警告：无法重新设置sys.stdout的编码")

# 定义全局变量以存储浏览器窗口的句柄
browser_hwnd = None

def open_browser():
    global browser_hwnd
    if browser_hwnd is None:
        windows = find_window_by_name("claude")
        if windows:
            browser_hwnd = windows[0]
            bring_window_to_front(browser_hwnd)
    else:
        bring_window_to_front(browser_hwnd)

def minimize_browser():
    global browser_hwnd
    if browser_hwnd:
        win32gui.ShowWindow(browser_hwnd, win32con.SW_MINIMIZE)
    else:
        print("未找到浏览器窗口")

def find_window_by_name(name):
    def callback(handle, data):
        if name.lower() in win32gui.GetWindowText(handle).lower():
            data.append(handle)
        return True
    result = []
    win32gui.EnumWindows(callback, result)
    return result
 
def bring_window_to_front(handle):
    if win32gui.IsIconic(handle):
        win32gui.ShowWindow(handle, win32con.SW_RESTORE)
        
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(handle)
        pythoncom.CoUninitialize()

def create_tray_icon():
    def on_quit():
        icon.stop()
        sys.exit()

    menu = Menu(
        MenuItem('退出', on_quit)
    )

    image = Image.new('RGB', (64, 64), color = (255, 0, 0))
    icon = Icon("browser_control", image, "claude", menu)
    icon.run()

def run_tray_icon():
    icon = create_tray_icon()
    icon.run()

if __name__ == "__main__":
    keyboard.add_hotkey('alt+c', open_browser)
    keyboard.add_hotkey('alt+m', minimize_browser)
    
    tray_thread = threading.Thread(target=run_tray_icon)
    tray_thread.daemon = True
    tray_thread.start()
    
    print("程序已启动，按 Ctrl+C 退出")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序正在退出...")
        sys.exit(0)
