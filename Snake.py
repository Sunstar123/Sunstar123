import pygame
import random
import time
# edit for your pleasure; uses RGB format: (R, G, B)
background_color = (240, 240, 240)
tail_color = (70, 70, 70)
head_color = (40, 40, 40)
grid_color = (220, 220, 220)
#
go_dict = {}
algorithm = ""
directions = []
width = 0
height = 0
win = pygame.display.init()
run = True
skip = 0
size = 0
area = []
begin_time = 0
finish_time = 0
died = False


class Snake:
    def __init__(self):
        self.length = 1  # length including head
        self.location = (int(0), int(0))  # head location
        self.tails = []  # contains all tail locations from oldest to youngest
        self.default = "right"  # starts game with default going right
        self.dont_dict = {"right": "left", "left": "right", "down": "up", "up": "down"}

    def move_auto_path(self):  # import snake ai here, or create another move function here
        go_not = self.dont_dict[self.default]
        try:
            self.default = go_dict[self.location]
            if self.default == go_not:  # cannot go backwards
                self.default = self.dont_dict[go_not]
        except KeyError:
            print("Invalid game configuration (try multiples of five?)")
        # print(self.default)
        # print(self.location)
        return self.default

    def move_auto_empty(self):  # empty snake ai
        return self.default

    def move_player(self):  # move manually
        global directions
        precedence = []
        go_not = self.dont_dict[self.default]
        for direction in directions:
            if direction == self.dont_dict[self.default]:  # snake cannot go backwards into itself
                pass
            elif direction == self.default:
                precedence.append(direction)
            else:
                precedence.insert(0, direction)
        if precedence:
            self.default = precedence[0]
        directions = []
        if self.default == go_not:
            self.default = self.dont_dict[go_not]
        return self.default

    def remove_last(self):
        area[self.tails[0][0]][self.tails[0][1]] = ""
        self.tails.pop(0)


def setup(mode=None, algorith=None, siz=None, ski=None):
    # To automatically do automatic setup change the following line to:     mode = "auto"
    # Or for manual setup                                                   mode = "manual"
    if not mode:
        mode = "ask user"
    # mode = "manual"
    # mode = "auto"
    #
    global win
    global width
    global height
    global skip
    global win
    global size
    global area
    global algorithm
    if algorith and siz and ski:
        print("Setting Up")
        print(f"Screen size: {siz}, Pixel skip: {ski}, Algorithm: {algorith}")
        algorithm = algorith
        size = siz
        skip = ski
        width = size * skip
        height = size * skip
        win = pygame.display.set_mode((width, height))
        for _ in range(0, int(width / skip)):
            out = []
            for _ in range(0, int(width / skip)):
                out.append("")
            area.append(out)
        pygame.init()
        print("Setup Completed")
        return
    if mode == "ask user":
        # print("\n\nTo control time scale:")  # time controls currently disable due to being unnecessary
        # print("speed 1.5 faster press '2', speed limits exist")
        # print("speed 1.5 slower press '1', speed limits exist\n")
        print("Welcome to snake, please create your settings (find the 'setup' function if typing 'auto'"
          " every run is too much work")
    while mode != "auto" and mode != "manual":
        mode = input("'auto' setup or 'manual' setup, (choose whether to play yourself, or have the ai play!)")
    if mode == "manual":
        success = False
        while not success:
            try:
                size = int(input("Enter a board size, MUST BE EVEN, non-zero: (recommended 20) "))
                skip = int(input("Enter the number of pixels per box, non-zero: (recommended: 25) "))
                ok = 'y'
                ok2 = 'y'
                if size > 50:
                    ok = input("This is a VERY big board size and might cause some problems, are you sure? 'y' / 'n'")
                if skip > 100:
                    ok = input("This is a VERY big pixel size and might cause some problems, are you sure? 'y' / 'n'")
                if ok == 'y' and ok2 == 'y' and size % 2 == 0 and size != 0 and skip != 0:
                    success = True
            except ValueError:
                pass
        width = size * skip
        height = size * skip
        algorithm = "empty"
        while algorithm != "player" and algorithm != "cpu":
            algorithm = input("would you like to player yourself: 'player' or have the cpu play: 'cpu'")
        if algorithm == "cpu":
            while algorithm != "cpuslow" and algorithm != "cpufast" and algorithm != "cpuhyper":
                algorithm += str(input("choose a speed: 'slow' or 'fast' or 'hyper'"))
    else:
        assert mode == "auto", "Setup Mode Error"
        size = 20
        skip = 25
        width = size * skip
        height = size * skip
        algorithm = "player"
        size = int(width / skip)
    win = pygame.display.set_mode((width, height))
    for _ in range(0, int(width / skip)):
        out = []
        for _ in range(0, int(width / skip)):
            out.append("")
        area.append(out)
    pygame.init()
    print("Setup Completed")


def generate_go_dict():
    print("generating moves")
    # time_before_generation = time.time()
    global go_dict
    global size
    global area
    if size == 2:
        go_dict[(0, 0)] = "right"
        go_dict[(1, 0)] = "down"
        go_dict[(1, 1)] = "left"
        go_dict[(0, 1)] = "up"
    else:
        for a, row in enumerate(area):
            for b, place in enumerate(row):
                if b == 0:  # first column
                    if a == 0:  # first row
                        direction = "right"
                    else:
                        direction = "up"
                elif a == 0 or a % 2 == 0:  # even row
                    if b == size - 1:  # end of row
                        direction = "down"
                    else:
                        direction = "right"
                else:  # odd row
                    assert a % 2 != 0, "even row in odd row???"
                    if b == 1:  # second column
                        if a == size - 1:
                            direction = "left"
                        else:
                            direction = "down"
                    else:
                        direction = "left"
                go_dict[(b, a)] = direction
    # print("moves generated in:", round(time.time() - time_before_generation, 4))


def rect_coord(x, y):
    global size
    global skip
    start_x = x * skip
    start_y = y * skip
    rect = (start_x + 1, start_y + 1, skip - 1, skip - 1)
    return rect


def move(to, snake, food_eaten):
    global size
    snake.tails.append(snake.location)
    area[snake.location[0]][snake.location[1]] = "tail"
    if not food_eaten:  # remove last segment if food has not been eaten
        snake.remove_last()
    # moving snake head and checking for collision with wall
    if to == "up":
        if snake.location[1] == 0:
            dead("wall")
            return
        else:
            snake.location = snake.location[0], snake.location[1] - 1
    elif to == "right":
        if snake.location[0] == size - 1:
            dead("wall")
            return
        else:
            snake.location = snake.location[0] + 1, snake.location[1]
    elif to == "left":
        if snake.location[0] == 0:
            dead("wall")
            return
        else:
            snake.location = snake.location[0] - 1, snake.location[1]
    else:
        assert to == "down", "move request not valid"
        if snake.location[1] == size - 1:
            dead("wall")
            return
        else:
            snake.location = snake.location[0], snake.location[1] + 1
    if area[snake.location[0]][snake.location[1]] == "food":
        snake.length += 1
        area[snake.location[0]][snake.location[1]] = "head"
        return "food_eaten"
    area[snake.location[0]][snake.location[1]] = "head"


def inputs():
    global run
    if algorithm == "player":
        global directions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    directions.append("right")
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    directions.append("left")
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    directions.append("up")
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    directions.append("down")
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


def tail_impact_check(snake):
    for tail_x, tail_y in snake.tails:  # tail drawing
        if snake.location[0] == tail_x and snake.location[1] == tail_y:
            dead("itself")
            return


def draw(snake, food):
    win.fill(background_color)
    global skip
    global size
    global width
    global height

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
    for tail_x, tail_y in snake.tails:  # tail drawing
        rect = rect_coord(tail_x, tail_y)
        pygame.draw.rect(win, tail_color, rect)  # draw every tail
    rect = rect_coord(snake.location[0], snake.location[1])
    pygame.draw.rect(win, head_color, rect)  # draw head
    if food:
        rect = rect_coord(food[0], food[1])
        pygame.draw.rect(win, (255, 0, 0), rect)  # draw food


def dead(cause):
    global run
    global died
    global finish_time
    if cause == "wall":
        print(f"\nThe snake hit a {cause}")
    else:
        if size == 2:
            run = False
            finish_time = time.time()
            return
        print(f"\nThe snake hit {cause}")
    died = True
    run = False


def cleanup_and_recording(algorith=None, siz=None, ski=None, screen=None):
    global died
    global finish_time
    pygame.quit()
    if algorith and siz and ski:
        if screen == "off" or screen is None or screen is False:
            screen = "off"
        else:
            screen = "on"
        with open("snake_records.txt", "a") as file:
            if not died:
                file.write(f"algorithm: {algorith}, size: {siz}, pixels per square: {ski}, screen: {screen}, time to "
                        f"finish: {round(finish_time - begin_time, 4)} seconds\n")
            else:
                assert died
                finish_time = time.time()
                file.write(f"algorithm: {algorith}, size: {siz}, pixels per square: {ski}, screen: {screen}, "
                        f"time to finish: {round(finish_time - begin_time, 4)} seconds, DIED\n")
    print("Finished")


def create_food(food, snake):
    global run
    global size
    global begin_time
    global finish_time
    if not food:  # if food exits create new food and return, else return food
        if snake.length >= size * size:
            if not finish_time:
                finish_time = time.time()
            return food, False
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        try:
            if size > 2:
                while area[x][y] == "tail" or area[x][y] == "head":
                    x = random.randint(0, size - 1)
                    y = random.randint(0, size - 1)
                area[x][y] = "fruit"
            else:
                while area[x][y] == "tail" or area[x][y] == "head":  # RIP
                    x = random.randint(0, size - 1)
                    y = random.randint(0, size - 1)
                    if snake.length > size * size - 2:
                        if not finish_time:
                            finish_time = time.time()
                        return food, False
                area[x][y] = "fruit"
        except IndexError:
            print(f"INDEX ERROR, bad index: ({x}, {y})")
            print("Number of rows", len(area), "Number of columns", len(area[0]))
            print(area)
            raise IndexError
        area[x][y] = "food"
        return (x, y), True
    else:
        found = False
        for each in area:
            for item in each:
                if item == "food":
                    found = True
        if not found:
            if snake.length < size * size:  # just in case the first time fails, which it shouldn't
                return create_food((), snake)
            else:
                if not finish_time:
                    finish_time = time.time()
                return food, False
        return food, False


def wait_time():
    global algorithm
    if algorithm == "player":
        tim = int(50 * 50 / size)
        pygame.time.wait(tim)
    elif algorithm[0:3] == "cpu":
        if algorithm[3:7] == "slow":
            tim = 300
        elif algorithm[3:7] == "fast":
            tim = 15
        elif algorithm[3:8] == "hyper":
            tim = None
        else:  # problem with input (or input was skipped), but assuming fast
            tim = None  # default 12
        if tim:
            pygame.time.wait(tim)
    else:  # this should not be possible
        print(algorithm[0:2])
        raise ValueError  # for lack of a better option


def main(mod=None, algorith=None, siz=None, ski=None, screen=None):
    setup(mod, algorith, siz, ski)
    global begin_time
    global finish_time
    global algorithm
    global area
    global run
    global head_color
    snake = Snake()
    food = ()
    last_printed_length = 0
    if algorithm == "player":
        pygame.time.wait(3000)  # game starts after 2 secs if in manual mode
    if algorithm[0:3] == "cpu":
        generate_go_dict()
        head_color = (0, 255, 0)
    begin_time = time.time()
    while run:
        if finish_time:  # if snake has finished
            run = False
            print("Time to finish:", round(finish_time - begin_time, 4), "seconds")
            break
        if not algorith and not siz and not ski:
            if snake.length % 5 == 0 and snake.length != last_printed_length:
                if snake.length <= 50 or snake.length % 20 == 0:
                    time_for_x = round(time.time() - begin_time, 4)
                    print(time_for_x)
                    predicted_time = round((int(size*size / snake.length) * time_for_x) / 60, 4)
                    print("predicted time to finish:", predicted_time, "minutes")
                    last_printed_length = snake.length
                    print(f"Snake Length Reached: {snake.length}/{size*size}")
        inputs()
        food, eaten = create_food(food, snake)  # returns cords of food and if food had been eaten
        # print(food, eaten)
        if algorithm == "player":
            res = move(snake.move_player(), snake, eaten)  # get snake move request and move
        elif algorithm[0:3] == "cpu":
            res = move(snake.move_auto_path(), snake, eaten)  # get snake move request and move
        else:
            res = move(snake.move_player(), snake, eaten)  # PLACEHOLDER for another algorithm
        if res == "food_eaten":
            food = ()
        if screen is None or screen is True or screen == "on":
            draw(snake, food)
            pygame.display.update()
        tail_impact_check(snake)
        if algorithm != "cpuhyper":
            wait_time()
    cleanup_and_recording(algorith, siz, ski, screen)


if __name__ == "__main__":
    for e in range(1):  # edit iterations of program here
        with open("snake_records.txt", "a") as f:
            time_now = str(time.strftime('%H:%M%p %Z on %b %d, %Y'))  # EDT
            if e != 0:
                f.write(f"Run at {time_now}\n")
            else:
                f.write(f"\nRun at {time_now}\n")
        for i in range(1, 7):  # edit iterations of program here
            go_dict = {}
            algorithm = ""
            directions = []
            width = 0
            height = 0
            win = pygame.display.init()
            run = True
            skip = 0
            size = 0
            area = []
            died = False
            begin_time = 0
            finish_time = 0
            print("\n")
            # main()  # normally run
            main(mod="auto", algorith="cpuhyper", siz=i*2, ski=10, screen=True)  # run specially
            # if AND ONLY IF all inputs are entered to the main method (aka. mode=w, algorith=x, siz=y, ski=z)
            # then manual user setup will be skipped
            #
            # mod: enter anything along with rest, or enter JUST mode with: "auto" or "manual" or "ask user"
            # algorith: for player control: "manual", for CPU control: "cpuhyper", "cpumedium", "cpuslow"
            # siz: size of squares on the board
            # ski: number of pixels per square
