from itertools import permutations
from random import randint
from math import dist
import pygame


class CityStorage:
    cities_one = [(781, 58), (425, 301), (622, 123), (402, 765), (646, 68), (155, 315), (652, 222), (372, 508), (783, 676), (182, 113), (8, 582), (425, 267), (382, 90), (769, 27), (585, 427), (461, 637), (176, 441)]


# return a list of x many points
def create_cities(number):
    # it helps to keep the max values below the resolution of the screen if you plan to visualize it
    return [(randint(0, 800), randint(0, 800)) for _ in range(number)]


# will always find the best answer, but unusably slow for high numbers of cities (cities > 10).
def shortest_path_brute(points):
    return round(min([path_distance(path) for path in permutations(points)]), 2)


# very fast and can handle extremely large numbers of cities, but often only finds a good answer not the best
def shortest_path_ants(points, iterations):
    pheromone_strength = 100  # amount of pheromone placed on every edge
    pheromone_loss = 1  # amount of pheromone lost on each edge after every ant
    # make big distance gains produce more pheromones?
    # should the pheromones be one way or two way? (currently against nature, one way)

    win = create_graph(points)

    edge_scores = dict()
    path_scores = list()
    best_path_distance = 2**62  # algorithm will break if best path distances exceed this number
    best_path = None

    for ant in range(iterations):
        # gradually dissipate pheromones
        for key in edge_scores.keys():
            if edge_scores[key] > 1:
                edge_scores[key] -= pheromone_loss
            if edge_scores[key] < 1:
                edge_scores[key] = 1

        path = simulate_ant(points[:], edge_scores)  # pass copy of points because the function edits it

        graph_ant(points, path, best_path, edge_scores, win)

        # place pheromones along each travelled edge if the path is good enough
        score = path_distance(path)
        path_scores.append(score)

        if score < best_path_distance:
            best_path = path
        if score <= best_path_distance:
            best_path_distance = score
            multiplier = 3
        # FIXME ideally this should consider numbers of better and worse scores, not the values of those scores
        elif score < .98 * best_path_distance:
            multiplier = 1.5
        elif score < .95 * best_path_distance:
            multiplier = 1
        elif score < .90 * best_path_distance:
            multiplier = .5
        elif score < .80 * best_path_distance:
            multiplier = .2
        else:
            multiplier = 0

        if multiplier != 0:
            for i in range(len(path) - 1):
                edge_scores[(path[i], path[i + 1])] = int(edge_scores.get((path[i], path[i + 1])) or 0) + int(pheromone_strength * multiplier)

    pygame.quit()
    return round(best_path_distance, 2)


# helper for finding the shortest path with an ant simulation
def simulate_ant(points, edge_scores):
    starting_pos = randint(0, len(points)-1)  # how to determine where to start? use pheromones to determine this too?
    path = [points[starting_pos]]
    del points[starting_pos]

    # choose which point to go to, repeat until travelled to all points
    for _ in range(len(points)):
        # method to determine which edge to go on:
        # sum the score of all edges and assign a range within that value to each edge
        # then pick a random number from 1 to that sum
        # then choose the edge for the range that the number falls into
        # edges with a value of 0 automatically get assigned a range of length 1 (should it be higher?)

        scores = [int(edge_scores.get((path[-1], point)) or 1) for point in points]

        # weird way of assigning a range to each value and picking the correct one
        num = randint(1, sum(scores))
        score_sum = 0
        next_point_loc = 2**62  # this line is totally unneeded and kinda shitty, but I hate warnings
        for i in range(len(scores)):
            score_sum += scores[i]
            if score_sum >= num:
                next_point_loc = i
                break

        path.append(points[next_point_loc])
        del points[next_point_loc]

    return path


# initialize pygame screen and add cities
def create_graph(points):
    pygame.init()
    pygame.display.set_caption("Travelling Salesman")
    x, y = zip(*points)
    win = pygame.display.set_mode((max(x) + 50, max(y) + 50))
    win.fill((255, 255, 255))
    pygame.display.update()

    return win


# update the graph for a new ant's path
def graph_ant(points, path, best_path, edge_scores, win):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # fill background with white
    win.fill((255, 255, 255))

    # draw cities
    for point in points:
        pygame.draw.circle(win, (0, 0, 0), point, 8)

    # draw path of best ant
    if best_path:
        for i in range(len(best_path) - 1):
            pygame.draw.line(win, (0, 0, 200), best_path[i], best_path[i + 1], 8)

    # draw path of last ant
    for i in range(len(path) - 1):
        pygame.draw.line(win, (40, 40, 40), path[i], path[i+1])

    # draw pheromone trails
    for key, value in edge_scores.items():
        if value > 1:
            color = ((value if value <= 255 else 255), 0, 0)
            pygame.draw.line(win, color, key[0], key[1], 3)

    pygame.display.update()
    # pygame.time.delay(50)  # slow things down to better see whats happening


# helper function to find the total distance to travel a path
def path_distance(path):
    total = 0
    for i in range(len(path) - 1):
        total += dist(path[i], path[i + 1])

    return total


def main():
    dots = create_cities(50)
    # dots = CityStorage.cities_one
    # distance = shortest_path_brute(dots)
    # print(distance)
    distance = shortest_path_ants(dots, 5000)
    print(distance)


if __name__ == '__main__':
    main()
