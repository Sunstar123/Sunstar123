import random


def fill_grid(highest, width, height):
    # if width * height < max:
    #     return  # max num won't fit
    result = [[0 for x in range(width)] for y in range(height)]
    order = [i for i in range(width * height)]
    random.shuffle(order)
    for i in range(1, highest + 1):
        result[int(order[-1] % width)][int(order[-1] / width)] = i
        order.pop()
    return result


grid = fill_grid(10, 5, 5)
for each in grid:
    print(each)
