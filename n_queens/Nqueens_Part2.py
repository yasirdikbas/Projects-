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

    ### ALL 4 DIAGNOLS CHECKED
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

# LasVegas algo for K queens which is a parameter
def LasVegasAlgo(grid, N, K):

    # amintainarray of available columns
    availableColumns = []
    columns = ['_' for i in range(N)]
    for i in range(1, N + 1):
        availableColumns.append(i)

    totalAvailable = N

    r = 0

    # while we have available columns and rows placd are less than K
    while totalAvailable > 0 and r < K:
        # choose randomly and place queen
        randCol = random.choice(availableColumns)

        totalAvailable -= 1
        availableColumns.remove(randCol)
        grid[r][randCol - 1] = 'Q'
        columns[r] = randCol

        r += 1

    # if board successful return True else False
    if checkBoardSuccessful(grid, N):
        return True
    return False

# Bactracking for rest K - 1 rows
def NQueen(grid, N, row):
    if row >= N:
        return True

    # if the current row has already queen placed it skips and goes to next row
    for col in range(N):
        if grid[row][col] == 'Q':
            NQueen(grid, N, row + 1)

    # backtracks if needed
    for col in range(N):
        if isSafe(grid, N, row, col):
            grid[row][col] = 'Q'
            if NQueen(grid, N, row + 1):
                return True
            grid[row][col] = '_'

    return False


def main():
    # for each K n times it performs numTrials and get probabilities
    numTrials = 10000
    N = [6, 8, 10]   # To be Set

    for n in N:
        K = n
        print(f'------------------- N = {n} ---------------------\n')
        for k in range(K):
            print('K = ' + str(k))

            successfulTrial = 0
            for i in range(10000):
                grid = [['_' for i in range(n)] for j in range(n)]

                trial = LasVegasAlgo(grid, n, k)

                if not trial:
                    continue

                trial = NQueen(grid, n, 0)
                if trial:
                    successfulTrial += 1
                    

            # prints stats for each K,N pair for numTrials
            print("\tNumber of successful placements : " + str(successfulTrial))
            print("\tNumber of Trials : " + str(numTrials))
            print("\tProbability that it will come to a solution : " +
                  str(float(successfulTrial / numTrials)))


if __name__ == "__main__":
    main()
