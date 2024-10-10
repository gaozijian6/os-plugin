import win32gui
import win32com.client
import win32con

def find_window_by_name(name):
    def callback(handle, data):
        if win32gui.GetWindowText(handle) == name:
            data.append(handle)
        return True
    result = []
    win32gui.EnumWindows(callback, result)
    return result

def bring_window_to_front(handle):
    if win32gui.IsIconic(handle):
        win32gui.ShowWindow(handle, win32con.SW_RESTORE)

    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(handle)

# 查找名为"claude"的窗口
handles = find_window_by_name("claude")

if handles:
    # 如果找到了窗口,将其置于前台
    handle = handles[0]
    bring_window_to_front(handle)
    print(f"已将名为'claude'的窗口置于前台,句柄为: {handle}")
else:
    print("未找到名为'claude'的窗口")