import numpy as np
import random


# program to print grid
def printGrid(grid):
    for row in grid:
        for col in row:
            print(col, end=" ")
        print()


# function to check if queen at (row,col) is safe from all
def isSafe(grid, N, row, col):
    # col check
    for i in range(N):
        if grid[row][i] == 'Q' and (not i == col):
            return False
    # row check
    for i in range(N):
        if grid[i][col] == 'Q' and (not i == row):
            return False

    # ALL 4 DIAGNOLS CHECKED
    i = row - 1
    j = col - 1
    while i >= 0 and j >= 0:
        if grid[i][j] == 'Q':
            return False
        i -= 1
        j -= 1

    i = row - 1
    j = col + 1
    while i >= 0 and j < N:
        if grid[i][j] == 'Q':
            return False
        i = i - 1
        j = j + 1

    i = row + 1
    j = col + 1
    while i < N and j < N:
        if grid[i][j] == 'Q':
            return False
        i = i + 1
        j = j + 1

    i = row + 1
    j = col - 1
    while i < N and j >= 0:
        if grid[i][j] == 'Q':
            return False
        i = i + 1
        j = j - 1

    return True


# check all queens are safe or not
def checkBoardSuccessful(grid, N):

    for row in range(N):
        for col in range(N):
            if grid[row][col] == 'Q':
                if not isSafe(grid, N, row, col):
                    return False

    return True


# LasVegas algo for all N rows
def LasVegasAlgo(N):
    # forms a grid and open output file
    f = open(f'results_{N}.txt', 'a')
    grid = [['_' for i in range(N)] for j in range(N)]

    # sets available columns
    availableColumns = []
    columns = ['_' for i in range(N)]
    for i in range(0, N):
        availableColumns.append(i)

    totalAvailable = N
    f.write('\n')

    r = 0
    step = 1

    # while we have available columns and Rows < N
    while totalAvailable > 0 and r < N:
        # chooses column randomly and uniformly
        randCol = random.choice(availableColumns)
        totalAvailable -= 1
        availableColumns.remove(randCol)
        grid[r][randCol] = 'Q'
        columns[r] = randCol

        f.write("Step - " + str(step) + " Columns : " + str(columns) + "\n")
        f.write("Step - " + str(step) +
                " Available Columns : " + str(availableColumns) + "\n")

        # after placig this queen if we check we are not having successful board until then we cannot have further so we break and return
        if not checkBoardSuccessful(grid, N):
            f.write("\nUnsuccessful\n\n")
            return False

        r += 1
        step += 1

    # checks if board is successful at the end to update successful trial
    successful = False
    if checkBoardSuccessful(grid, N):
        f.write("\nSuccessful\n")
        successful = True
    else:
        f.write("\nUnsuccessful\n\n")

    f.close()

    return successful


def main():

    # num of trials = 
    numTrials = 10000
    successfulTrial = 0
    N = 10   # To be Set

    f = open(f'results_{N}.txt', 'w')
    f.close()

    # running algo for mentioned N numTrial times
    for i in range(numTrials):
        trial = LasVegasAlgo(N)
        if trial:
            successfulTrial += 1

    # printing stats
    print("Las Vegas Algorithm with N = " + str(N))
    print("Number of successful placements : " + str(successfulTrial))
    print("Number of Trials : " + str(numTrials))
    print("Probability that it will come to a solution : " +
          str(float(successfulTrial / numTrials)))


if __name__ == "__main__":
    main()
