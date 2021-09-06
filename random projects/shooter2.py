from PIL import ImageGrab
import keyboard
import numpy as np
import time
import cv2
import random
# noinspection PyUnresolvedReferences
import MouseKeys
#  how to find the coordinates of anything:
#  go to python console and paste in:
#
#  import pyautogui
#  pyautogui.position()
#
#  ^ prints the x and y coords of mouse ^
# game_coords = (653, 582, 1153, 762)  # coords of the game screen where attackers actually appear, towards bottom right
# game_coords2 = (660, 356, 1153, 762)  # coords of screen starting at top left of the health bar towards bottom right
pause = False
no_go_zone = []
items_dict = {"game_coords": (0, 260, 458, 408), "start_button": (430, 320), "ammo": (12, 20),
              "retry_button": (300, 270), "check_for_shop": (5, 3), "clip_buy": (60, 100),
              "repair_buy": (140, 100), "wall_buy": (230, 100), "sniper_buy": (310, 100),
              "fortify_buy": (400, 100), "gunman_buy": (50, 270), "craftsman_buy": (130, 270),
              "missle_buy": (220, 270), "done": (310, 400)}
try:
    with open("shooterWave.txt", "r") as f:
        wave = int(f.read())
except ValueError:
    print("ERROR")
    wave = 25  # so that even in the case of a mess up, high level runs are not compromised


def setup_vars(game_x, game_y):
    global items_dict
    items_dict["start"] = (game_x, game_y)
    keys_to_edit = []
    for key, item in items_dict.items():
        if str(key) != "game_coords" and str(key) != "start" and str(key) != "ammo":
            keys_to_edit.append(key)
    for item in keys_to_edit:
        items_dict[item] = (items_dict[item][0] + game_x, items_dict[item][1] + game_y)
    # for key, value in items_dict.items():
    #     pass
    items_dict["start"] = items_dict["start"][0], items_dict["start"][1] + 582 - 356


def find_game_coords():
    window = ImageGrab.grab()
    width, height = window.size
    for x in range(width):
        for y in range(height):
            color = window.getpixel((x, y))
            if color == (204, 153, 51):
                if window.getpixel((x + 550, y)) == (204, 153, 51):  # secondary check for incase of random pixels
                    # pyautogui._mouseMoveDrag("drag", x, y, 0, 0, .01)
                    print("Found Game")
                    return x, y
    print("ERROR: Game Window Not Found")
    return False


def screenshot(game_x, game_y):
    global items_dict
    time_before = time.time()
    cords = (game_x, game_y, game_x + items_dict["game_coords"][2], game_y + items_dict["game_coords"][3])
    screen = ImageGrab.grab(bbox=cords)
    r, g, b = screen.getpixel(items_dict["ammo"])
    if 550 < r + g + b < 700:
        check_ammo()
    width, height = screen.size
    screen = screen.crop(box=(0, items_dict["game_coords"][1], width, height))
    items_dict["end"] = screen.size
    screen = np.array(screen)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    # print("elapsed time:", round(time.time() - time_before, 4))
    return screen, time_before


def bubble(x, y):
    global no_go_zone
    global items_dict
    if len(no_go_zone) != 0:
        for i, zone in enumerate(no_go_zone):
            # print(i, len(no_go_zone))
            no_go_zone[i] = (no_go_zone[i][0], no_go_zone[i][1], no_go_zone[i][2] + 1)
            if no_go_zone[i][2] >= 40:
                no_go_zone.pop(i)
    try:
        for bx, by, _ in no_go_zone:
            bubble_size = 38
            # print(bx, by, x, y)
            if bx - bubble_size < x < bx + bubble_size:
                if by - bubble_size < y < by + bubble_size:
                    # print("fail")
                    return False
        no_go_zone.append((x, y, 0))
        # print("success")
        return True
    except ValueError:
        no_go_zone.append((x, y, 0))
        return True


def do_it(screen, time_before):
    global items_dict
    global wave
    start = items_dict["start"]
    end = items_dict["end"]
    if screen[items_dict["check_for_shop"][0] - start[0]][items_dict["check_for_shop"][1] - start[1]] == 23:
        return "Died"
    if 40 > screen[items_dict["check_for_shop"][0] - start[0]][items_dict["check_for_shop"][1] - start[1]] > 10:
        return "Shop"
    skip = 6
    for x in range(5, end[0] - 5, skip):
        for y in range(5, end[1] - 5, skip):
            if screen[end[1] - y][end[0] - x] < 10:
                actual_x = start[0] + end[0] - x + 6
                actual_y = start[1] + end[1] - y + 32
                if wave > 13:
                    MouseKeys.click(actual_x, actual_y)
                elif wave > 8:
                    if bubble(actual_x, actual_y):
                        MouseKeys.click(actual_x, actual_y)
                        MouseKeys.click(actual_x, actual_y)
                    else:
                        MouseKeys.click(actual_x, actual_y, "n")  # so that ammo is refilled
                        if random.randint(1, 100) > 95:
                            return
                else:
                    if bubble(actual_x, actual_y):
                        MouseKeys.click(actual_x, actual_y)
                        MouseKeys.click(actual_x, actual_y)
                        print("elapsed time:", round(time.time() - time_before, 4))
                        return
                    else:
                        MouseKeys.click(actual_x, actual_y, "n")
                        return
    print("elapsed time:", round(time.time() - time_before, 4))


def menu():
    global pause
    global items_dict
    keyboard.press_and_release('space')
    if pause:
        while not keyboard.is_pressed('h'):
            time.sleep(1)
    pause = False
    for i in range(50):  # buy health
        time.sleep(.01)
        MouseKeys.click(*items_dict["repair_buy"])
        if keyboard.is_pressed('p'):
            print("'p' pressed")
            break
    for i in range(10):  # buy bullets
        # time.sleep(.01)
        MouseKeys.click(items_dict["clip_buy"][0], items_dict["clip_buy"][1])
    if wave < 20:  # buy specials, default order:
        MouseKeys.click(items_dict["sniper_buy"][0], items_dict["sniper_buy"][1])  # sniper
        MouseKeys.click(items_dict["wall_buy"][0], items_dict["wall_buy"][1])  # wall
        MouseKeys.click(items_dict["fortify_buy"][0], items_dict["fortify_buy"][1])  # fortify
    for i in range(20 * wave):  # buy bullets
        MouseKeys.click(items_dict["clip_buy"][0], items_dict["clip_buy"][1])
    MouseKeys.click(items_dict["done"][0], items_dict["done"][1])  # exit menu
    keyboard.press('space')
    time.sleep(2)


def check_ammo():
    for i in range(10):
        keyboard.press_and_release("space")
        # MouseKeys.PressKey(0x39)
        # MouseKeys.ReleaseKey(0x39)
        time.sleep(.001)
    # print("SPACE")


def restart():
    global wave
    global items_dict
    print(f"Died on wave {wave}")
    died = f"died on wave: {wave}\n"
    with open("data.txt", "a") as file:
        file.write(died)
    time.sleep(5)
    MouseKeys.click(*items_dict["retry_button"])
    time.sleep(1)
    MouseKeys.click(*items_dict["start_button"])


def main():
    time_beforee = time.time()
    global wave
    global pause
    global items_dict
    try:
        game_x, game_y = find_game_coords()
        # game_x, game_y = 652, 324
        setup_vars(game_x, game_y)
        MouseKeys.click(*items_dict["start_button"])
        time.sleep(4)
    except TypeError:
        return
        # game_x, game_y = 652, 324
        # setup_vars(game_x, game_y)
    print("setup time:", round(time.time() - time_beforee, 4))
    run = True
    while run:
        MouseKeys.ReleaseKey(0x39)
        result = do_it(*screenshot(game_x, game_y))
        # result = False
        if result == "Shop":
            wave += 1
            print(f"Wave: {wave}, at: Shop")
            menu()
        elif result == "Died":
            print("Died")
            restart()
        if keyboard.is_pressed('p'):
            print("'p' pressed")
            run = False
        if keyboard.is_pressed('m'):
            print("'m' pressed, will pause or not pause at next shop")
            if pause:
                pause = False
            else:
                pause = True
        if keyboard.is_pressed('s'):
            screen = ImageGrab.grab(bbox=items_dict["game_coords"])
            screen = np.array(screen)
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            print(screen[0][0])
    with open("shooterWave.txt", "w") as fi:
        fi.write(str(wave))


# MouseKeys.ReleaseKey(0x39)
main()
# MouseKeys.ReleaseKey(0x39)
print("finished")
