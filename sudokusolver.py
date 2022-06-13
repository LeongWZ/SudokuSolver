import time


class Solution(object):
    def makeCoordinatesGroupTable(self, board):
        groupings = [[] for i in range(9)]

        for i, y in enumerate(board):
            for j, x in enumerate(y):
                if 0 <= i <= 2 and 0 <= j <= 2:
                    groupings[0].append((i, j))
                elif 0 <= i <= 2 and 3 <= j <= 5:
                    groupings[1].append((i, j))
                elif 0 <= i <= 2 and 6 <= j <= 8:
                    groupings[2].append((i, j))
                elif 3 <= i <= 5 and 0 <= j <= 2:
                    groupings[3].append((i, j))
                elif 3 <= i <= 5 and 3 <= j <= 5:
                    groupings[4].append((i, j))
                elif 3 <= i <= 5 and 6 <= j <= 8:
                    groupings[5].append((i, j))
                elif 6 <= i <= 8 and 0 <= j <= 2:
                    groupings[6].append((i, j))
                elif 6 <= i <= 8 and 3 <= j <= 5:
                    groupings[7].append((i, j))
                elif 6 <= i <= 8 and 6 <= j <= 8:
                    groupings[8].append((i, j))

        coordinatesGroupTable = {}
        for group in groupings:
            for index, coordinates in enumerate(group):
                l = group.copy()
                l.pop(index)
                coordinatesGroupTable[coordinates] = l

        return coordinatesGroupTable

    def findGroup_3x3(self, i, j, coordinatesGroupTable):
        return coordinatesGroupTable[(i, j)]

    def inGroup_3x3(self, i, j, board, coordinatesGroupTable):
        if board[i][j] == '.':
            return False

        group_3x3 = self.findGroup_3x3(i, j, coordinatesGroupTable)
        for coordinates in group_3x3:
            if board[coordinates[0]][coordinates[1]] == board[i][j]:
                return True

        return False

    def inColumn(self, i, j, board):
        if board[i][j] == '.':
            return False

        # searching above
        ref_i = i - 1
        while ref_i >= 0:
            if board[ref_i][j] == board[i][j]:
                return True
            ref_i -= 1

        # searching below
        ref_i = i + 1
        while ref_i <= 8:
            if board[ref_i][j] == board[i][j]:
                return True
            ref_i += 1

        return False

    def inRow(self, i, j, board):
        if board[i][j] == '.':
            return False

        # searching left
        ref_j = j - 1
        while ref_j >= 0:
            if board[i][ref_j] == board[i][j]:
                return True
            ref_j -= 1

        # searching right
        ref_j = j + 1
        while ref_j <= 8:
            if board[i][ref_j] == board[i][j]:
                return True
            ref_j += 1

        return False

    def isValid(self, i, j, board, coordinatesGroupTable):
        if self.inColumn(i, j, board):
            return False
        if self.inRow(i, j, board):
            return False
        if self.inGroup_3x3(i, j, board, coordinatesGroupTable):
            return False
        return True

    def makeEmptyList(self, board):
        emptyList = []
        for i, y in enumerate(board):
            for j, x in enumerate(y):
                if board[i][j] == '.':
                    emptyList.append((i, j))
        return emptyList

    def makeHistory(self, emptyList):
        history = {}
        for empty in emptyList:
            i, j = empty[0], empty[1]
            history[(i, j)] = None
        return history

    def transpose(self, board):
        transposedBoard = [list(i) for i in zip(*board)]
        for i, y in enumerate(board):
            for j, x in enumerate(board):
                board[i][j] = transposedBoard[i][j]

    def mirror(self, board):
        mirrorBoard = [i[::-1] for i in board]
        for i, y in enumerate(board):
            for j, x in enumerate(board):
                board[i][j] = mirrorBoard[i][j]

    def scanForward(self, board, columnStop):
        emptyCounter = 0
        if columnStop == -1:
            indexCounter = 0
            for j, x in enumerate(board[0]):
                if x == '.':
                    emptyCounter += 1
                    indexCounter += j
            return (emptyCounter, indexCounter)

        elif columnStop == 4:
            for i, y in enumerate(board[:columnStop+1]):
                if i != 4:
                    for x in y:
                        if x == '.':
                            emptyCounter += 1
                else:
                    for x in y[:5]:
                        if x == '.':
                            emptyCounter += 1
        else:
            for y in board[:columnStop+1]:
                for x in y:
                    if x == '.':
                        emptyCounter += 1
        return emptyCounter

    def scanBackward(self, board, columnStop):
        emptyCounter = 0
        if columnStop == -1:
            indexCounter = 0
            for j, x in enumerate(board[::-1][0][::-1]):
                if x == '.':
                    emptyCounter += 1
                    indexCounter += j
            return (emptyCounter, indexCounter)
        elif columnStop == 4:
            for i, y in enumerate(board[::-1][:columnStop+1]):
                if i != 4:
                    for x in y:
                        if x == '.':
                            emptyCounter += 1
                else:
                    for x in y[4:]:
                        if x == '.':
                            emptyCounter += 1
        else:
            for y in board[::-1][:columnStop+1]:
                for x in y:
                    if x == '.':
                        emptyCounter += 1

        return emptyCounter

    def getDirection(self, board, columnStop=4, count_startTopLeft_goRight=True, count_startBottomRight_goLeft=True, count_startTopLeft_goDown=True, count_startBottomRight_goUp=True,
                    count_startTopRight_goLeft=True, count_startBottomLeft_goRight=True, count_startTopRight_goDown=True, count_startBottomLeft_goUp=True):
        
        counters = {}

        if count_startTopLeft_goRight:
            counters['startTopLeft_goRight'] = self.scanForward(board, columnStop)
        if count_startBottomRight_goLeft:
            counters['startBottomRight_goLeft'] = self.scanBackward(board, columnStop)

        self.transpose(board)
        if count_startTopLeft_goDown:
            counters['startTopLeft_goDown'] = self.scanForward(board, columnStop)
        if count_startBottomRight_goUp:
            counters['startBottomRight_goUp'] = self.scanBackward(board, columnStop)
        self.transpose(board)
            
        self.mirror(board)
        if count_startTopRight_goLeft:
            counters['startTopRight_goLeft'] = self.scanForward(board, columnStop)
        if count_startBottomLeft_goRight:
            counters['startBottomLeft_goRight'] = self.scanBackward(board, columnStop)

        self.transpose(board)
        if count_startTopRight_goDown:
            counters['startTopRight_goDown'] = self.scanForward(board, columnStop)
        if count_startBottomLeft_goUp:
            counters['startBottomLeft_goUp'] = self.scanBackward(board, columnStop)
        self.transpose(board)
        self.mirror(board)

        if columnStop == -1:
            smallestEmptyCounter = min(counters.values(), key=lambda x: x[0])[0]
            emptyTie = {}
            for k in counters.keys():
                if counters[k][0] == smallestEmptyCounter:
                    emptyTie[k] = counters[k]

            if len(emptyTie) == 1:
                for k in emptyTie.keys():
                    return k

            largestIndexCounter = max(emptyTie.values(), key=lambda x: x[1])[1]
            indexTie = {}
            for k in emptyTie.keys():
                if emptyTie[k][1] == largestIndexCounter:
                    indexTie[k] = emptyTie[k]
            for k in indexTie.keys():
                return k
        else:
            smallestEmptyCounter = min(counters.values())
            emptyTie = {}
            for k in counters.keys():
                if counters[k] == smallestEmptyCounter:
                    emptyTie[k] = counters[k]

            if len(emptyTie) == 1:
                for k in emptyTie.keys():
                    return k
                    
            count_startTopLeft_goRight = False
            count_startBottomRight_goLeft = False
            count_startTopLeft_goDown = False
            count_startBottomRight_goUp = False
            count_startTopRight_goLeft = False
            count_startBottomLeft_goRight = False
            count_startTopRight_goDown = False
            count_startBottomLeft_goUp = False

            for k in emptyTie.keys():
                if k == 'startTopLeft_goRight':
                    count_startTopLeft_goRight = True
                elif k == 'startBottomRight_goLeft':
                    count_startBottomRight_goLeft = True
                elif k == 'startTopLeft_goDown':
                    count_startTopLeft_goDown = True
                elif k == 'startBottomRight_goUp':
                    count_startBottomRight_goUp = True
                elif k == 'startTopRight_goLeft':
                    count_startTopRight_goLeft = True
                elif k == 'startBottomLeft_goRight':
                    count_startBottomLeft_goRight = True
                elif k == 'startTopRight_goDown':
                    count_startTopRight_goDown = True
                elif k == 'startBottomLeft_goUp':
                    count_startBottomLeft_goUp = True

            return self.getDirection(board, columnStop-1, count_startTopLeft_goRight, count_startBottomRight_goLeft, count_startTopLeft_goDown, count_startBottomRight_goUp,
                                    count_startTopRight_goLeft, count_startBottomLeft_goRight, count_startTopRight_goDown, count_startBottomLeft_goUp)

    def goForward(self, board):
        coordinatesGroupTable = self.makeCoordinatesGroupTable(board)
        emptyList = self.makeEmptyList(board)
        history = self.makeHistory(emptyList)

        x = 0
        while x < len(emptyList):
            empty = emptyList[x]
            i, j = empty[0], empty[1]

            if history[(i,j)] is None:
                startNumber = 1
            else:
                startNumber = history[(i,j)] + 1

            for number in range(startNumber, 10):
                board[i][j] = str(number)
                if self.isValid(i, j, board, coordinatesGroupTable):
                    history[(i,j)] = number
                    x += 1
                    break
            else:
                board[i][j] = '.'
                history[(i,j)] = None
                x -= 1
                if x < 0:
                    raise Exception('x cannot be below 0')

    def goBackward(self, board):
        coordinatesGroupTable = self.makeCoordinatesGroupTable(board)
        emptyList = self.makeEmptyList(board)
        history = self.makeHistory(emptyList)

        counter = 0
        x = len(emptyList) - 1
        while x >= 0:
            counter += 1
            empty = emptyList[x]
            i, j = empty[0], empty[1]

            if history[(i,j)] is None:
                startNumber = 1
            else:
                startNumber = history[(i,j)] + 1

            for number in range(startNumber, 10):
                board[i][j] = str(number)
                if self.isValid(i, j, board, coordinatesGroupTable):
                    history[(i,j)] = number
                    x -= 1
                    break
            else:
                board[i][j] = '.'
                history[(i,j)] = None
                x += 1
                if x >= len(emptyList):
                    raise Exception('x cannot be above or equal to length of emptyList')

    def startTopLeft_goRight_traverse(self, board):
        """
        starts from top left hand corner and traverses right
        """
        try:
            self.goForward(board)
        except Exception as e:
            raise e

    def startBottomRight_goLeft_traverse(self, board):
        """
        starts from bottom right hand corner and traverses left
        """
        try:
            self.goBackward(board)
        except Exception as e:
            raise e
    
    def startTopLeft_goDown_traverse(self, board):
        """
        starts from top left hand corner and traverses down
        """
        try:
            self.transpose(board)
            self.goForward(board)
            self.transpose(board)
        except Exception as e:
            raise e

    def startBottomRight_goUp_traverse(self, board):
        """
        starts from bottom right hand corner and traverses up
        """
        try:
            self.transpose(board)
            self.goBackward(board)
            self.transpose(board)
        except Exception as e:
            raise e

    def startTopRight_goLeft_traverse(self, board):
        """
        starts from top right hand corner and traverses left
        """
        try:
            self.mirror(board)
            self.goForward(board)
            self.mirror(board)
        except Exception as e:
            raise e

    def startBottomLeft_goRight_traverse(self, board):
        """
        starts from bottom left hand corner and traverses right
        """
        try:
            self.mirror(board)
            self.goBackward(board)
            self.mirror(board)
        except Exception as e:
            raise e

    def startTopRight_goDown_traverse(self, board):
        """
        starts from top right hand corner and traverses down
        """
        try:
            self.mirror(board)
            self.transpose(board)
            self.goForward(board)
            self.transpose(board)
            self.mirror(board)
        except Exception as e:
            raise e

    def startBottomLeft_goUp_traverse(self, board):
        """
        starts from bottom left hand corner and traverses up
        """
        try:
            self.mirror(board)
            self.transpose(board)
            self.goBackward(board)
            self.transpose(board)
            self.mirror(board)
        except Exception as e:
            raise e

    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: None Do not return anything, modify board in-place instead.
        """
        direction = self.getDirection(board)

        try:
            if direction == 'startTopLeft_goRight':
                self.startTopLeft_goRight_traverse(board)
            elif direction == 'startBottomRight_goLeft':
                self.startBottomRight_goLeft_traverse(board)
            elif direction == 'startTopLeft_goDown':
                self.startTopLeft_goDown_traverse(board)
            elif direction == 'startBottomRight_goUp':
                self.startBottomRight_goUp_traverse(board)
            elif direction == 'startTopRight_goLeft':
                self.startTopRight_goLeft_traverse(board)
            elif direction == 'startBottomLeft_goRight':
                self.startBottomLeft_goRight_traverse(board)
            elif direction == 'startTopRight_goDown':
                self.startTopRight_goDown_traverse(board)
            elif direction == 'startBottomLeft_goUp':
                self.startBottomLeft_goUp_traverse(board)

        except Exception as e:
            raise e


def processInput(sudokuInput):
    # process format
    sudokuArray = []
    for j, s in enumerate(sudokuInput):
        if j % 9 == 0:
            sudokuArray.append([])
        sudokuArray[-1].append(s)

    # prints input in new format
    print('Input:')
    for row in sudokuArray:
        print(row)

    # prints solution
    print('')
    print('Solution:')
    solution = Solution()
    start = time.time()
    try:
        solution.solveSudoku(sudokuArray)
        end = time.time()
        for row in sudokuArray:
            print(row)
    except Exception as e:
        end = time.time()
        print(f'No solution; {e}')

    print('')
    print(f'Runtime: {round((end - start) * 1000)} ms')

    # prints separation
    print('-'*50)
    print('')

def main():
    print('Sudoku Solver')
    print('By LeongWZ')
    print('')
    # Example on using the program
    print('For example,')
    print('')
    print('if sudoku is:')
    print(['5', '3', '.', '.', '7', '.', '.', '.', '.'])
    print(['6', '.', '.', '1', '9', '5', '.', '.', '.'])
    print(['.', '9', '8', '.', '.', '.', '.', '6', '.'])
    print(['8', '.', '.', '.', '6', '.', '.', '.', '3'])
    print(['4', '.', '.', '8', '.', '3', '.', '.', '1'])
    print(['7', '.', '.', '.', '2', '.', '.', '.', '6'])
    print(['.', '6', '.', '.', '.', '.', '2', '8', '.'])
    print(['.', '.', '.', '4', '1', '9', '.', '.', '5'])
    print(['.', '.', '.', '.', '8', '.', '.', '7', '9'])
    print('')
    print('input should be:')
    print('input > 53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
    print('')
    print('')

    while True:
        sudokuInput = input('input > ')
        print('')
        processInput(sudokuInput)
        print('')

if __name__ == "__main__":
    main()
    
