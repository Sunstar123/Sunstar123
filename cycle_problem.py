
file = open("data.txt")
data = file.readlines()
rooms = int(data[0])
starting_room = int(data[1])
location = starting_room


def walk(doors):
    global rooms
    global location
    for i in range(doors):
        if location == rooms:
            location = 0
        else:
            location += 1
    if location >= rooms / 2:
        return True
    else:
        return False


def solve():
    global rooms
    walk_amount = rooms / 4
    lower_bound, upper_bound = (0, rooms)
    for i in range(10):
        result = walk(walk_amount)
        if result:
            pass
        else:
            pass
