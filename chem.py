import random
# matplotlib used only for graphing, disable if unavailable
from matplotlib import pyplot as plt
import numpy as np
#


# simulates any number of 50-50 coin flips
def random_heads(to_flip):
    total = 0
    for _ in range(to_flip):
        total += random.randint(0, 1)
    return total


# creates data by doing runs of coin flipping
def run(starting, amount):
    runs = []
    for _ in range(amount):
        heads = starting
        iterations = 0
        while heads != 0:
            heads = random_heads(heads)
            # print(f"Run: {iterations}, Heads this run: {heads}")
            try:
                runs[iterations].append(heads)
            except IndexError:
                runs.append([heads])
            iterations += 1
    return runs


# graphing
def graph_things(avgs):
    # requires matplotlib if not available disable the import and this function
    x = range(len(avgs))
    y = avgs
    plt.title("Tossing Heads")
    plt.xlabel("Tosses")
    plt.ylabel("Heads")
    plt.plot(x, y)
    # plt.plot(range(2, 18), [1/2**i for i in range(2, 18)])  # graph 1/2^x
    plt.plot(x, y, 'o')  # show data points
    plt.show()


# main
def main():
    starting_heads = 500
    times_to_run = 1000
    data = run(starting_heads, times_to_run)
    averages = [starting_heads]

    print(f"Ran {times_to_run} times with {starting_heads} starting heads each time.")
    for i in range(len(data)):
        average = sum(data[i]) / times_to_run
        runs_with_heads = len(data[i])
        runs_with_heads_percentage = 100 * runs_with_heads / times_to_run
        if runs_with_heads >= 10:  # don't utilize data with too few data points
            averages.append(average)
        print(f"Loop: {i + 1}, Average: {average}, runs with heads: {runs_with_heads}"
              f" ({runs_with_heads_percentage}%)")

    graph_things(averages)


# start execution
if __name__ == "__main__":
    main()
