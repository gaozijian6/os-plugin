import keyboard
import subprocess
import time
import win32gui
import win32con

# 定义全局变量以存储浏览器窗口的句柄
browser_hwnd = None

# 遍历所有窗口，查找谷歌浏览器的窗口
def find_browser_window():
    global browser_hwnd
    def enum_window_callback(hwnd, _):
        window_text = win32gui.GetWindowText(hwnd)
        if "Google Chrome" in window_text:
            print(f"找到窗口: {window_text}, 句柄: {hwnd}")
            global browser_hwnd
            browser_hwnd = hwnd
            return False  # 找到窗口后停止遍历
        return True  # 继续遍历其他窗口

    win32gui.EnumWindows(enum_window_callback, None)

def open_browser():
    global browser_hwnd
    # 打开谷歌浏览器
    subprocess.Popen(['start', 'chrome'], shell=True)
    time.sleep(1)
    find_browser_window()

def minimize_browser():
    global browser_hwnd
    if browser_hwnd is not None:
        win32gui.ShowWindow(browser_hwnd, win32con.SW_MINIMIZE)
    else:
        print("未找到谷歌浏览器窗口")

# 设置快捷键
keyboard.add_hotkey('alt+c', open_browser)
keyboard.add_hotkey('alt+m', minimize_browser)

print("按下 alt+c 打开浏览器，按下 alt+m 缩小浏览器窗口")
keyboard.wait('esc')  # 按下 Esc 键退出程序
