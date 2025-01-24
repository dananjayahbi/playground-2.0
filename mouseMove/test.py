import pyautogui
import time

def move_mouse():
    while True:
        x, y = pyautogui.position()  # Get current mouse position
        pyautogui.moveTo(x + 30, y + 30, duration=0.5)  # Move slightly
        pyautogui.moveTo(x, y, duration=0.5)  # Move back to original position
        print("Mouse moved to prevent sleep.")
        time.sleep(900)  # Wait for 15 minutes (900 seconds)

if __name__ == "__main__":
    move_mouse()
