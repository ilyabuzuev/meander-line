import matplotlib.pyplot as plt
import random
import math

cellSize = 3
cellsCount = 2
# cellsMap = [[1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1],
#             [2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2],
#             [3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3],
#             [2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2],
#             [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]]

# cellsMap = [[1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1],
#             [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1],
#             [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1],
#             [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1],
#             [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]]

width = cellsCount
length = cellsCount

xCoords = [0]
yCoords = [0]

x0 = 0
y0 = 0


def getCurrentCoords():
  return x0, y0

def move(direction, value):
  x, y = getCurrentCoords()

  # print(value)

  global x0
  global y0

  if (direction == 'up'):
    x0 = x
    y0 += value

  if (direction == 'down'):
    x0 = x
    y0 -= value
  
  if (direction == 'right'):
    x0 += value
    y0 = y

  if (direction == 'left'):
    x0 -= value
    y0 = y

  xCoords.append(x0)
  yCoords.append(y0)

def createCellsMap(widthX, widthY):
  cellsMap = []

  maxRowNum = math.ceil(widthX / 2)
  mid = math.ceil(widthY / 2)

  for i in range(mid):
    row = []

    for j in range(widthX):
      if (i < mid):
        if (j < maxRowNum):
          row.append(j + 1 + i)
        else:
          row.append(widthX - j + i)

    cellsMap.append(row)

  temp = cellsMap[::-1]
  
  if (widthY % 2 != 0):
    temp.pop(0)

  res = cellsMap + temp

  return res

# print( createCellsMap(18, 9) )

def createCell(branchesNumber, row, currCell, cellCount, cellSize):
  lineLength = cellSize
  offset = cellSize * 1 / (branchesNumber + 2)

  commandParams = ['right', 'down', 'left', 'up']
  movementCommands = []

  i = 0
  while (i < branchesNumber + 3):
    movementCommands.append(commandParams[i % 4])
    i += 1

  temp = movementCommands[::-1]
  temp.pop(0)
  res = movementCommands + temp

  if (row % 2 != 0):
    for i in range(len(res)):
      if (res[i] == 'right'):
        res[i] = 'left'
        continue

      if (res[i] == 'left'):
        res[i] = 'right'
        continue

      if (res[i] == 'up'):
        res[i] = 'down'
        continue

      if (res[i] == 'down'):
        res[i] = 'up'
        continue

  if (row % 2 == 0):
    move('up', lineLength)

  for i in range(len(res)):
    if (i <= math.floor(len(res) / 2)):
      if (i == 0):
        move(res[i], lineLength)
      elif (i > 0 and i < math.floor(len(res) / 2) - 1):
        move(res[i], lineLength - offset)
        lineLength -= offset
      else:
        move(res[i], lineLength - offset)
    else:
      if (i == len(res) - 1):
        move(res[i], lineLength)
      elif (i > math.floor(len(res) / 2) - 1 and i < len(res) - 2):
        move(res[i], lineLength - offset)
        lineLength += offset
      else:
        move(res[i], lineLength - offset)

  if (row % 2 != 0 and currCell != cellCount - 1):
    move('down', lineLength)

# def createRandomCellsMap(min, max, length):
#   for i in range(length):
#     cellsMap.append(random.randint(min, max))

# createRandomCellsMap(1, 10, cellsCount)

cellsMap = createCellsMap(11, 7)

for row in range(len(cellsMap)):
  for cell in range(len(cellsMap[row])):
    createCell(cellsMap[row][cell], row, cell, len(cellsMap[row]), cellSize)

  if (row % 2 == 0):
    move('up', cellSize + cellSize * 1 / 10)
  elif (row != len(cellsMap) - 1):
    move('up', cellSize * 1 / 10)

# print(xCoords, yCoords)

plt.plot(xCoords, yCoords)
plt.show()