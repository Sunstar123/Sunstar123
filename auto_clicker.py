import keyboard
import pyautogui


def clicker():
    start_key = "s"
    pause_key = "p"
    quit_key = "q"
    while True:
        if keyboard.is_pressed(start_key):
            break
    run = True
    while run:
        if keyboard.is_pressed(quit_key):
            print("quiting")
            run = False
        if not keyboard.is_pressed(pause_key):
            pyautogui.click()


# starts when start key pressed and continues until quit key pressed
# pauses when pause key is help down
clicker()
