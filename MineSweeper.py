import pygame
import random
import time

show_bombs = False  # change to "True" to reveal everything
show_numbers = False

height = 1000
width = height  # must be the same as height
skip = 100  # pixels per square
size = int(height / skip)  # number of boxes
background_color = (240, 240, 240)
background_color_plus = (230, 230, 230)  # unactivated tiles
grid_color = (220, 220, 220)
pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mine Sweeper')
pygame.display.set_icon(pygame.image.load("mine.png"))
run = True
area = []
bomb_color = (0, 0, 0)
max_bombs = int(size * size / 10)
button_list = []
font_size = 70
turn = 0
directions = [(- 1, 0), (1, 0), (0, - 1), (0, 1), (- 1, 1), (-1, -1), (1, 1), (1, -1)]
color_dict = {"1": (30, 30, 230), "2": (30, 230, 30), "3": (230, 30, 30), "4": (148, 0, 211), "5": (100, 100, 100),
              "6": (30, 30, 30), "7": (30, 30, 30), "8": (30, 30, 30)}


class Button:
    def __init__(self, position, coord):
        self.size = skip
        self.position = position  # pixel coordinates
        self.coordinates = coord  # game board coordinates
        self.down = False


def button_pressed(button_press, position):
    if button_press == 1 or button_press == 3:  # button 2 is mouse wheel, which is unneeded
        for button in button_list:
            if button.position[0] + skip > position[0] > button.position[0]:
                if button.position[1] + skip > position[1] > button.position[1]:
                    if button_press == 1:
                        reveal(button.coordinates)
                    else:
                        assert button_press == 3
                        x, y = button.coordinates
                        if not area[0][0] == "":  # make sure board is activated
                            if not area[x][y][2] or area[x][y][3]:  # if not activated
                                if not area[x][y][3]:
                                    area[x][y] = (area[x][y][0], area[x][y][0], area[x][y][0], True)  # flag True
                                else:
                                    area[x][y] = (area[x][y][0], area[x][y][0], False, False)  # flag False


def inputs():
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button_pressed(event.button, event.pos)
        else:  # do not care about other events
            pass


def rect_coord(x, y):
    global size
    global skip
    start_x = x * skip
    start_y = y * skip
    rect = (start_x + 1, start_y + 1, skip - 1, skip - 1)
    return rect


def generate_objects(x_2, y_2):
    time_start = time.time()
    # print("Setting up board")
    bomb_count = 0
    # generate bombs
    # no_bombs_direction = (random.randint(1, 2), random.randint(1, 2))
    while bomb_count < max_bombs:
        for x, row in enumerate(area):
            for y, item in enumerate(row):
                if random.randint(1, size * size) == size * size:  # size * size = number of tiles
                    if bomb_count < max_bombs and not item:  # testing if bomb already exists here
                        if x_2 - 2 < x < x_2 + 2 and y_2 - 2 < y < y_2 + 2:
                            pass
                        else:
                            bomb_count += 1
                            area[x][y] = ("bomb", bomb_color, show_bombs, False)
    # generate numbers
    for x, row in enumerate(area):
        for y, item in enumerate(row):
            if not item:  # if no bombs here
                bombs_near = 0
                for loc in directions:
                    try:
                        if size - 1 >= loc[0] + x >= 0 and size - 1 >= loc[1] + y >= 0:
                            if area[loc[0] + x][loc[1] + y][0] == "bomb":
                                bombs_near += 1
                    except IndexError:
                        pass
                if bombs_near == 0:  # even when in debug mode empty squares should not be shown
                    area[x][y] = (str(bombs_near), str(bombs_near), False, False)
                else:
                    area[x][y] = (str(bombs_near), str(bombs_near), show_numbers, False)
    time_end = time.time()
    # print(f"Board set up in {round(time_end - time_start, 4)} seconds\n")


def generate_buttons():
    for i in range(size + 1):  # actually runs for the number of square
        start_x = i * skip
        for e in range(size + 1):
            start_y = e * skip
            button_list.append(Button((start_x, start_y), (i, e)))


def draw_grid():
    win.fill(background_color)
    for w in range(size + 1):
        start_position = (0, w * skip)
        end_position = (width, w * skip)
        pygame.draw.line(win, grid_color, start_position, end_position)
        if w == size:  # draw last grid lines
            start_position = (0, w * skip - 1)
            end_position = (width, w * skip - 1)
            pygame.draw.line(win, grid_color, start_position, end_position)
    for w in range(size + 1):
        start_position = (w * skip, 0)
        end_position = (w * skip, height)
        pygame.draw.line(win, grid_color, start_position, end_position)
        if w == size:  # draw last grid lines
            start_position = (w * skip - 1, 0)
            end_position = (w * skip - 1, height)
            pygame.draw.line(win, grid_color, start_position, end_position)


def draw_objects():
    font = pygame.font.Font('freesansbold.ttf', font_size)
    for x, row in enumerate(area):
        for y, item in enumerate(row):
            if item[3]:
                text = font.render("F", True, (0, 0, 0))
                rect = rect_coord(x, y)
                text_rect = text.get_rect()
                text_rect.center = (int(rect[0] + int(skip / 2)), int(rect[1] + int(skip / 2)))
                win.blit(text, text_rect)
            elif item[2]:
                if item[1] == "0":  # empty squares
                    pass
                elif item[0] != "bomb":
                    text = font.render(item[1], True, color_dict[item[1]])
                    rect = rect_coord(x, y)
                    text_rect = text.get_rect()
                    text_rect.center = (int(rect[0] + int(skip / 2)), int(rect[1] + int(skip / 2)))
                    win.blit(text, text_rect)
                else:  # numbered square
                    text = font.render("B", True, (0, 0, 0))
                    rect = rect_coord(x, y)
                    text_rect = text.get_rect()
                    text_rect.center = (int(rect[0] + int(skip / 2)), int(rect[1] + int(skip / 2)))
                    win.blit(text, text_rect)
            else:
                coordinates = rect_coord(x, y)
                pygame.draw.rect(win, background_color_plus, coordinates)
    position = pygame.mouse.get_pos()
    for button in button_list:
        if button.position[0] + skip > position[0] > button.position[0]:
            if button.position[1] + skip > position[1] > button.position[1]:
                if not area[button.coordinates[0]][button.coordinates[1]][2]:
                    bbox = (button.position[0], button.position[1], skip, skip)
                    pygame.draw.rect(win, (255, 255, 255), bbox)


def reveal_empty(to_empty_list):
    new_check = to_empty_list
    updated = False
    for each in to_empty_list:
        x, y = each
        for direction in directions:
            x_check = x + direction[0]
            y_check = y + direction[1]
            area[x][y] = (area[x][y], area[x][y][1], True, area[x][y][3])
            if 0 <= x_check <= size - 1 and 0 <= y_check <= size - 1:
                if area[x_check][y_check][0] != "0" and area[x_check][y_check][0] != "bomb":
                    area[x_check][y_check] = (area[x_check][y_check][0], area[x_check][y_check][1],
                                          True, area[x_check][y_check][3])  # edit visibility: to True
                if not (x_check, y_check) in new_check:  # does set already contain this
                    if area[x_check][y_check][0] == "0" and not area[x_check][y_check][2]:
                        new_check.append((x + direction[0], y + direction[1]))
                        updated = True

    if updated:
        reveal_empty(new_check)


def check_won():
    global run
    won = True
    for row in area:
        for item in row:
            if not item[2]:
                if not item[0] == "bomb":
                    won = False
    if won:
        # print("HOLY JESUS YOU DID IT OMG GOOD JOB")
        run = False


def reveal(coordinates):
    global run
    global turn
    turn += 1
    x = coordinates[0]
    y = coordinates[1]
    if area[0][0] == "":
        generate_objects(x, y)
    if area[x][y][0] == "bomb":
        # print("YOU HIT A BOMB")
        run = False
    else:
        if area[x][y][0] == "0":
            # if it was a flag, cancel that
            area[x][y] = (area[x][y][0], area[x][y][1], area[x][y][2], False)
            reveal_empty([(x, y)])
        else:
            # if it was a flag, cancel that
            # make it visible
            area[x][y] = (area[x][y][0], area[x][y][1], True, False)
    check_won()


def cleanup():
    # print("Game Over")
    pygame.quit()


def main():
    for _ in range(0, int(width / skip)):
        out = []
        for _ in range(0, int(width / skip)):
            out.append("")
        area.append(out)
    generate_buttons()
    global run
    run = True
    while run:
        # time_start = time.time()
        draw_grid()
        if not area[0][0] == "":
            draw_objects()
        pygame.display.update()
        time_end = time.time()
        # print(f"Frame rendered in {round(time_end - time_start, 4)} seconds")
        pygame.time.wait(100)
        inputs()
    cleanup()


if __name__ == "__main__":
    main()
