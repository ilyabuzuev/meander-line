import matplotlib.pyplot as plt
import math
from tkinter import *

class DielectricFiller:
  def __init__(self):
    self.state = 'INIT'

    self.xCoords = [0]
    self.yCoords = [0]

    self.x0 = 0
    self.y0 = 0

    self.defaultCellSize = 5
    self.defaultWidthX = 11 
    self.defaultWidthY = 7

    self.root = Tk()

  def getCurrentState(self):
    return self.state
  
  def setState(self, state):
    self.state = state

    self.nextState()

  def nextState(self):
    currentState = self.getCurrentState()

    if (currentState == 'INIT'):
      return self.start()

    if (currentState == 'CALCULATE_LINES_TRACE'):
      return self.calculateLinesTrace()
    
    if (currentState == 'PLOT_GRAPHS'):
      return self.plotGraphs()
    
    print(currentState)

  def getCurrentCoords(self):
    return self.x0, self.y0

  def move(self, direction, value):
    x, y = self.getCurrentCoords()

    if (direction == 'up'):
      self.x0 = x
      self.y0 += value

    if (direction == 'down'):
      self.x0 = x
      self.y0 -= value
    
    if (direction == 'right'):
      self.x0 += value
      self.y0 = y

    if (direction == 'left'):
      self.x0 -= value
      self.y0 = y

    self.xCoords.append(self.x0)
    self.yCoords.append(self.y0)

  def createCellsMap(self, widthX, widthY):
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
    # return [
    #   [1, 1, 2, 2, 3, 2, 2, 1, 1],
    #   [1, 1, 2, 2, 3, 2, 2, 1, 1],
    #   [1, 1, 2, 2, 3, 2, 2, 1, 1],
    #   [1, 1, 2, 2, 3, 2, 2, 1, 1],
    #   [1, 1, 2, 2, 3, 2, 2, 1, 1]
    # ]

  def createCell(self, branchesNumber, row, currCell, cellCount, cellSize):
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
      self.move('up', lineLength)

    for i in range(len(res)):
      if (i <= math.floor(len(res) / 2)):
        if (i == 0):
          self.move(res[i], lineLength)
        elif (i > 0 and i < math.floor(len(res) / 2) - 1):
          self.move(res[i], lineLength - offset)
          lineLength -= offset
        else:
          self.move(res[i], lineLength - offset)
      else:
        if (i == len(res) - 1):
          self.move(res[i], (lineLength - (cellSize * 1 / (branchesNumber + 2))) + cellSize * 1 / 8)
        elif (i > math.floor(len(res) / 2) - 1 and i < len(res) - 2):
          self.move(res[i], lineLength - offset)
          lineLength += offset
        else:
          self.move(res[i], lineLength - offset)

    if (row % 2 != 0 and currCell != cellCount - 1):
      self.move('down', lineLength)

  def calculateLinesTrace(self, cellSize=3, widthX=11, widthY=7):
    self.state = 'CALCULATE_LINES_TRACE'

    cellsMap = self.createCellsMap(widthX, widthY)

    print(cellsMap)

    for row in range(len(cellsMap)):
      for cell in range(len(cellsMap[row])):
        self.createCell(cellsMap[row][cell], row, cell, len(cellsMap[row]), cellSize)

      if (row % 2 == 0):
        self.move('up', cellSize + cellSize * 1 / 10)
      elif (row != len(cellsMap) - 1):
        self.move('up', cellSize * 1 / 8)

    print(self.getCurrentState())

    self.setState('PLOT_GRAPHS')

    return widthX, widthY

  def plotGraphs(self, widthX=11, widthY=7):
    self.state = 'PLOT_GRAPHS'

    plt.figure(figsize=(widthX, widthY))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(self.xCoords, self.yCoords)
    plt.show()

    self.xCoords = [0]
    self.yCoords = [0]

    self.x0 = 0
    self.y0 = 0

    print(self.getCurrentState())

    self.setState('INIT')

  def start(self):
    print(self.getCurrentState())

    self.root.title('Диэлектрический наполнитель')
    self.root['bg'] = '#deecfa'
    self.root.geometry('500x200')
    self.root.resizable(width=False, height=False)

    inputCellSizeLbl = Label(self.root, text='Размер ячейки (мм):', fg='#222', bg='#deecfa', font='Arial 14')
    inputCellSizeLbl.grid(column=0, row=0, padx=5, pady=5)

    defaultCellSizeValue = IntVar(self.root, value=self.defaultCellSize)
    inputCellSize = Entry(self.root, bg='white', fg='#222', font='Arial 14', textvariable=defaultCellSizeValue)
    inputCellSize.grid(column=1, row=0, padx=5, pady=5)

    inputCellsNumberOnX = Label(self.root, text='К-во ячеек по оси X:', fg='#222', bg='#deecfa', font='Arial 14')
    inputCellsNumberOnX.grid(column=0, row=1, padx=5, pady=5)

    defaultXValue = IntVar(self.root, value=self.defaultWidthX)
    cellsNumberOnX = Entry(self.root, bg='white', fg='#222', font='Arial 14', textvariable=defaultXValue)
    cellsNumberOnX.grid(column=1, row=1, padx=5, pady=5)

    inputCellsNumberOnY = Label(self.root, text='К-во ячеек по оси Y:', fg='#222', bg='#deecfa', font='Arial 14')
    inputCellsNumberOnY.grid(column=0, row=2, padx=5, pady=5)

    defaultYValue = IntVar(self.root, value=self.defaultWidthY)
    cellsNumberOnY = Entry(self.root, bg='white', fg='#222', font='Arial 14', textvariable=defaultYValue)
    cellsNumberOnY.grid(column=1, row=2, padx=5, pady=5)

    btn = Button(self.root, text='Рассчитать', bg='#b2d3f3', fg='#222', borderwidth=0, command=lambda: self.calculateLinesTrace(float(inputCellSize.get()), int(cellsNumberOnX.get()), int(cellsNumberOnY.get())), font='Arial 14')
    btn.grid(row=3, sticky="nsew", padx=5, pady=5)

    self.root.mainloop()
    
meander = DielectricFiller()
meander.setState('INIT')
