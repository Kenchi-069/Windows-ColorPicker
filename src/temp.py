import ctypes
import tkinter as tk
import keyboard

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse_position():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def get_pixel_color(x, y):
    hdc = user32.GetDC(0)
    color = gdi32.GetPixel(hdc, x, y)
    user32.ReleaseDC(0, hdc)
    r = color & 0xFF
    g = (color >> 8) & 0xFF
    b = (color >> 16) & 0xFF
    return r, g, b

def show_hex_popup(hex_code):
    root = tk.Tk()
    root.title("Pixel Color")
    root.geometry("220x120")
    root.resizable(False, False)

    root.attributes('-topmost', True)
    label = tk.Label(root, text=f"HEX: {hex_code}", font=("Arial", 16))
    label.pack(pady=10)

    def copy_to_clipboard():
        root.clipboard_clear()
        root.clipboard_append(hex_code)
        root.update()
        print(f"{hex_code} copied to clipboard!")

    copy_btn = tk.Button(root, text="Copy", command=copy_to_clipboard)
    copy_btn.pack(pady=10)

    root.mainloop()

def pick_color_on_click():
    print("Click anywhere to get pixel HEX (Press ESC to exit)...")
    while True:
        if user32.GetAsyncKeyState(0x02) & 0x8000:  # Left click
            x, y = get_mouse_position()
            r, g, b = get_pixel_color(x, y)
            hex_code = f"#{r:02X}{g:02X}{b:02X}"
            print(f"Clicked at ({x},{y}) → {hex_code}")
            show_hex_popup(hex_code)
        elif keyboard.is_pressed('esc'):  # Global ESC detection
            print("Cancelled by user.")
            break
        ctypes.windll.kernel32.Sleep(50)  # prevent CPU hogging

keyboard.add_hotkey('ctrl+shift+k', pick_color_on_click)

# Keep script running in background
keyboard.wait()  # waits forever until the program is terminated