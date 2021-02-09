import time

maxQueens = 8

def verifyPos(newColPos, rowPos):
    for colPos in range(newColPos):
        if queens[colPos] == rowPos or abs(colPos - newColPos) == abs(queens[colPos] - rowPos):
            return False
    return True

def placeQueen(maxQ, colPos=0):
    global counter
    if colPos == maxQ:
        counter += 1
        print(counter, queens)
    else:
        for rowPos in range(1, maxQ + 1):
            if verifyPos(colPos, rowPos):
                queens[colPos] = rowPos
                placeQueen(maxQ, colPos + 1)

counter = 0
queens = [0] * maxQueens

start = time.ticks_us()
placeQueen(maxQueens)
end = time.ticks_us()

print('{} results in {} ms'.format(counter, (end - start) / 1000))
