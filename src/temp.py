import ctypes

user32 = ctypes.windll.user32 #user input
gdi32 = ctypes.windll.gdi32 #color pixel retrieval
kernel32 = ctypes.windll.kernel32 #memory management

UNICODE = 13 #Windows constant meaning clipboard contains unicode text

class POINT(ctypes.Structure): #class definition for point
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

import ctypes

user32 = ctypes.windll.user32
CF_UNICODETEXT = 13

def copy_to_clipboard(text):
    # Open and empty clipboard
    user32.OpenClipboard(0)
    user32.EmptyClipboard()

    # Create a Unicode buffer for the text
    buf = ctypes.create_unicode_buffer(text)

    # Set clipboard data directly
    if not user32.SetClipboardData(CF_UNICODETEXT, ctypes.cast(buf, ctypes.c_void_p)):
        user32.CloseClipboard()
        raise OSError("SetClipboardData failed")

    user32.CloseClipboard()


# Define a POINT structure
def get_mouse_position():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def get_hex_code(x, y):
    hdc = user32.GetDC(0) #get accss to screen
    color = gdi32.GetPixel(hdc, x, y)
    user32.ReleaseDC(0, hdc)

    r = color & 0xFF
    g = (color >> 8) & 0xFF
    b = (color >> 16) & 0xFF
    return (r, g, b) 

def getColorOnClick():
    print("Click anywhere to copy that pixel's hash value")
    while True:
        if user32.GetAsyncKeyState(0x01) & 0x8000:  # Left mouse button pressed
            x, y = get_mouse_position()
            r, g, b = get_hex_code(x, y)
            hex_code = f"#{r:02X}{g:02X}{b:02X}"
            copy_to_clipboard(hex_code)
            print(f"({x}, {y}) - {hex_code} (copied!)")
            kernel32.Sleep(150)
        elif user32.GetAsyncKeyState(0x1B) & 0x8000:
            print("Exiting....")
            break

getColorOnClick()