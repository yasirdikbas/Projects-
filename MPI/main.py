# Enes Gülşen 2019400312
# Yasir Dikbaş 2019400051
# Compilation status : Compiling
# Working status: Working

from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
psize = size - 1  # number of processors

f = open(sys.argv[1])
dataLine = f.readline()
dataArray = []

for s in dataLine.split(' '):
    dataArray.append(s)
mapSize = int(dataArray[0])
waveSize = int(dataArray[1])
noOfTowers = int(dataArray[2])
resultArray = [["." for x in range(mapSize)] for y in range(mapSize)]  # stores map to create ultimate output


def simulation(rank, data, above, below, mapSize):  # simulates game for each round
    for i in range(int(mapSize / psize)):
        for j in range(mapSize):
            if data[i][j][0] == "o":
                try:
                    if data[i][j + 1][0] == "+":
                        data[i][j][1] -= 2
                except:
                    pass
                try:
                    if data[i][j - 1][0] == "+" and j != 0:
                        data[i][j][1] -= 2
                except:
                    pass
                try:
                    if data[i + 1][j][0] == "+":
                        data[i][j][1] -= 2
                except:
                    pass
                try:
                    if data[i - 1][j][0] == "+" and i != 0:
                        data[i][j][1] -= 2
                except:
                    pass
                if i == (mapSize / psize - 1):
                    try:
                        if below[j][0] == "+":
                            data[i][j][1] -= 2
                    except:
                        pass
                if i == 0:
                    try:
                        if above[j][0] == "+":
                            data[i][j][1] -= 2
                    except:
                        pass

            if data[i][j][0] == "+":
                try:
                    if data[i][j + 1][0] == "o":
                        data[i][j][1] -= 1
                except:
                    pass
                try:
                    if data[i][j - 1][0] == "o" and j != 0:
                        data[i][j][1] -= 1
                except:
                    pass
                try:
                    if data[i + 1][j][0] == "o":
                        data[i][j][1] -= 1
                except:
                    pass
                try:
                    if data[i - 1][j][0] == "o" and i != 0:
                        data[i][j][1] -= 1
                except:
                    pass
                try:
                    if data[i + 1][j + 1][0] == "o":
                        data[i][j][1] -= 1
                except:
                    pass
                try:
                    if data[i + 1][j - 1][0] == "o" and j != 0:
                        data[i][j][1] -= 1
                except:
                    pass
                try:
                    if data[i - 1][j + 1][0] == "o" and i != 0:
                        data[i][j][1] -= 1
                except:
                    pass
                try:
                    if data[i - 1][j - 1][0] == "o" and i != 0 and j != 0:
                        data[i][j][1] -= 1
                except:
                    pass
                if i == (mapSize / psize - 1):
                    try:
                        if below[j][0] == "o":
                            data[i][j][1] -= 1
                    except:
                        pass
                    try:
                        if below[j - 1][0] == "o" and j != 0:
                            data[i][j][1] -= 1
                    except:
                        pass

                    try:
                        if below[j + 1][0] == "o":
                            data[i][j][1] -= 1
                    except:
                        pass
                if i == 0:
                    try:
                        if above[j][0] == "o":
                            data[i][j][1] -= 1
                    except:
                        pass

                    try:
                        if above[j - 1][0] == "o" and j != 0:
                            data[i][j][1] -= 1
                    except:
                        pass
                    try:
                        if above[j + 1][0] == "o":
                            data[i][j][1] -= 1
                    except:
                        pass

    for i in range(int(mapSize / psize)):
        for j in range(mapSize):
            try:
                if data[i][j][1] <= 0:
                    data[i][j][1] = 0
                    data[i][j][0] = "."
            except:
                pass


for i in range(waveSize):
    towerArray = [[["." for x in range(2)] for y in range(mapSize)] for z in range(mapSize)]  # original map
    for j in range(2):
        dataLine = f.readline()
        dataArray = []
        for line in dataLine.split(", "):
            for s in line.split(' '):
                dataArray.append(s)
            if j == 0:
                towerArray[int(dataArray[0])][int(dataArray[1])][0] = "o"
                towerArray[int(dataArray[0])][int(dataArray[1])][1] = 6
            else:
                towerArray[int(dataArray[0])][int(dataArray[1])][0] = "+"
                towerArray[int(dataArray[0])][int(dataArray[1])][1] = 8
            dataArray.clear()
    # splits the map and sends its corresponding parts to the processors for each wave
    for p in range(1, size):
        if rank == p:
            below = []
            above = []
            if i == 0:  # first wave : no need to chech for overwrite
                data = towerArray[int(mapSize * ((p - 1) / psize)):int(mapSize * (p / psize))]
            else:  # other waves: checks if overwriting possible
                for k in range(int(mapSize / psize)):
                    for l in range(mapSize):
                        if data[k][l][0] == ".":
                            data[k][l] = towerArray[k + int(mapSize * ((p - 1) / psize))][l]

    # data exchange between processors and game simulation for each round
    for rounds in range(8):
        if rank != 0 and rank % 2 == 0 and rank < size:  # even numbered processors
            comm.send(data[0], dest=rank - 1)
            above = comm.recv(source=rank - 1)
            if rank != psize:
                comm.send(data[int(mapSize / psize) - 1], dest=rank + 1)
                below = comm.recv(source=rank + 1)
            simulation(rank, data, above, below, mapSize)
        elif rank % 2 == 1 and rank < size:  # odd numbered processors
            comm.send(data[int(mapSize / psize) - 1], dest=rank + 1)
            below = comm.recv(source=rank + 1)
            if rank != 1:
                comm.send(data[0], dest=rank - 1)
                above = comm.recv(source=rank - 1)
            simulation(rank, data, above, below, mapSize)

# sends result of the game to manager processor
for i in range(1, size):
    if rank == i:
        comm.send(data, dest=0, tag=i)
for j in range(1, size):
    if rank == 0:
        resultArray[int(mapSize * ((j - 1) / psize)):int(mapSize * (j / psize))] = comm.recv(source=j, tag=j)
    else:
        continue
    outputFile = open(sys.argv[2], "w")
    # prints result map to a text file
    for i in range(mapSize):
        for s in range(mapSize):
            outputFile.write(resultArray[i][s][0])
            if s != mapSize - 1:
                outputFile.write(" ")
        if i != mapSize - 1:
            outputFile.write("\n")
