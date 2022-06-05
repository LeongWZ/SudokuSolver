# sudoku solver

import time


def makeCoordinatesGroupTable():
    g1 = [
            (0,0), (0,1), (0,2),
            (1,0), (1,1), (1,2),
            (2,0), (2,1), (2,2)
         ]
    g2 = [
            (0,3), (0,4), (0,5),
            (1,3), (1,4), (1,5),
            (2,3), (2,4), (2,5)
         ]
    g3 = [
            (0,6), (0,7), (0,8),
            (1,6), (1,7), (1,8),
            (2,6), (2,7), (2,8)
         ]
    g4 = [
            (3,0), (3,1), (3,2),
            (4,0), (4,1), (4,2),
            (5,0), (5,1), (5,2)
         ]
    g5 = [
            (3,3), (3,4), (3,5),
            (4,3), (4,4), (4,5),
            (5,3), (5,4), (5,5)
         ]
    g6 = [
            (3,6), (3,7), (3,8),
            (4,6), (4,7), (4,8),
            (5,6), (5,7), (5,8)
         ]
    g7 = [
            (6,0), (6,1), (6,2),
            (7,0), (7,1), (7,2),
            (8,0), (8,1), (8,2)
         ]
    g8 = [
            (6,3), (6,4), (6,5),
            (7,3), (7,4), (7,5),
            (8,3), (8,4), (8,5)
         ]
    g9 = [
            (6,6), (6,7), (6,8),
            (7,6), (7,7), (7,8),
            (8,6), (8,7), (8,8)
         ]

    coordinatesGroupTable = dict()
    groupings = [g1, g2, g3, g4, g5, g6, g7, g8, g9]
    for group in groupings:
        for index, coordinates in enumerate(group):
            l = group.copy()
            l.pop(index)
            coordinatesGroupTable[coordinates] = l

    return coordinatesGroupTable

def findGroup_3x3(i, j, coordinatesGroupTable):
    return coordinatesGroupTable[(i,j)]

def inGroup_3x3(i, j, board, coordinatesGroupTable):
    if board[i][j] == '.':
        return False

    group_3x3 = findGroup_3x3(i, j, coordinatesGroupTable)
    for coordinates in group_3x3:
        if board[coordinates[0]][coordinates[1]] == board[i][j]:
            return True

    return False

def inColumn(i, j, board):
    if board[i][j] == '.':
        return False

    # searching above
    ref_i = i-1
    while ref_i >= 0:
        if board[ref_i][j] == board[i][j]:
            return True
        ref_i -= 1

    # searching below
    ref_i = i+1
    while ref_i <= 8:
        if board[ref_i][j] == board[i][j]:
            return True
        ref_i += 1

    return False

def inRow(i, j, board):
    if board[i][j] == '.':
        return False

    # searching left
    ref_j = j-1
    while ref_j >= 0:
        if board[i][ref_j] == board[i][j]:
            return True
        ref_j -= 1

    # searching right
    ref_j = j+1
    while ref_j <= 8:
        if board[i][ref_j] == board[i][j]:
            return True
        ref_j += 1

    return False

def isValid(i, j, board, coordinatesGroupTable):
    if inGroup_3x3(i, j, board, coordinatesGroupTable):
        return False
    if inColumn(i, j, board):
        return False
    if inRow(i, j, board):
        return False
    return True

def makeEmptyList(board):
    emptyList = []
    for i, y in enumerate(board):
            for j, x in enumerate(y):
                if board[i][j] == '.':
                    emptyList.append((i,j))
    return emptyList

def makeHistory(emptyList):
    history = {}
    for empty in emptyList:
        i, j = empty[0], empty[1]
        history[(i,j)] = None
    return history

def sudokuSolver(board):
    start = time.time()

    coordinatesGroupTable = makeCoordinatesGroupTable()
    emptyList = makeEmptyList(board)
    history = makeHistory(emptyList)

    solution = board.copy()
    
    x = 0
    while x < len(emptyList):
        empty = emptyList[x]
        i, j = empty[0], empty[1]

        if history[(i,j)] is None:
            startNumber = 1
        else:
            startNumber = history[(i,j)] + 1

        for number in range(startNumber, 10):
            solution[i][j] = str(number)
            if isValid(i, j, solution, coordinatesGroupTable):
                history[(i,j)] = number
                x += 1
                break
        else:
            solution[i][j] = '.'
            history[(i,j)] = None
            x -= 1
            if x < 0:
                end = time.time()
                print(f'(time taken: {round((end-start) * 1000)} ms)')
                raise Exception('x cannot be below 0')

    end = time.time()
    print(f'(time taken: {round((end-start) * 1000)} ms)')
    return solution


def processTestCases(testCases):
    for testCase in testCases:
        # process format
        for i, board in enumerate(testCase):
            testArray = []
            for j, s in enumerate(board):
                if j % 9 == 0:
                    testArray.append([])
                testArray[-1].append(s)
            testCase[i] = testArray

        # prints input in new format
        print('input:')
        test = testCase[0]
        for row in test:
            print(row)

        # prints result
        print('solution:')
        try: 
            result = sudokuSolver(test)
            for row in result:
                print(row)
        except Exception as e:
            result = 'No solution'
            print(f'{result}; {e}')

        # checks if result matches with given solution
        try:
            solution = testCase[1]
            print(result == solution)
        except IndexError:
            pass
        
        # prints separation
        print('-'*50)
        print('')

def processInput(input):
    # process format
    inputArray = []
    for j, s in enumerate(input):
        if j % 9 == 0:
            inputArray.append([])
        inputArray[-1].append(s)

    # prints input in new format
    print('input:')
    for row in inputArray:
        print(row)

    # prints result
    print('solution:')
    try: 
        result = sudokuSolver(inputArray)
        for row in result:
            print(row)
    except Exception as e:
        result = 'No solution'
        print(f'{result}; {e}')
    
    # prints separation
    print('-'*50)
    print('')
        
def main():
    print('Sudoku Solver')
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
        inputSudoku = input('input > ')
        print('')
        processInput(inputSudoku)
        print('')

validTestCases = [
                ['974236158638591742125487936316754289742918563589362417867125394253649871491873625',
                '974236158638591742125487936316754289742918563589362417867125394253649871491873625'
                ],     
                ['2564891733746159829817234565932748617128.6549468591327635147298127958634849362715',
                '256489173374615982981723456593274861712836549468591327635147298127958634849362715'
                ],
                ['3.542.81.4879.15.6.29.5637485.793.416132.8957.74.6528.2413.9.655.867.192.965124.8',
                '365427819487931526129856374852793641613248957974165283241389765538674192796512438'
                ],
                ['..2.3...8.....8....31.2.....6..5.27..1.....5.2.4.6..31....8.6.5.......13..531.4..',
                '672435198549178362831629547368951274917243856254867931193784625486592713725316489'
                ],
                ['53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79',
                '534678912672195348198342567859761423426853791713924856961537284287419635345286179']
            ]

invalidTestCases = [
                    ['.................................................................................'],
                    ['........................................1........................................'],
                    ['...........5....9...4....1.2....3.5....7.....438...2......9.....1.4...6..........'],
                    ['..9.7...5..21..9..1...28....7...5..1..851.....5....3.......3..68........21.....87'],
                    ['6.159.....9..1............4.7.314..6.24.....5..3....1...6.....3...9.2.4......16..'],
                    ['..9.287..8.6..4..5..3.....46.........2.71345.........23.....5..9..4..8.7..125.3..'],
                    ['.9.3....1....8..46......8..4.5.6..3...32756...6..1.9.4..1......58..2....2....7.6.'],
                    ['....41....6.....2...2......32.6.........5..417.......2......23..48......5.1..2...'],
                    ['9..1....4.14.3.8....3....9....7.8..18....3..........3..21....7...9.4.5..5...16..3'],
                    ['.39...12....9.7...8..4.1..6.42...79...........91...54.5..1.9..3...8.5....14...87.'],
                    ['..3.....6...98..2.9426..7..45...6............1.9.5.47.....25.4.6...785...........'],
                    ['....9....6..4.7..8.4.812.3.7.......5..4...9..5..371..4.5..6..4.2.17.85.9.........'],
                    ['59.....486.8...3.7...2.1.......4.....753.698.....9.......8.3...2.6...7.934.....65'],
                    ['...3165..8..5..1...1.89724.9.1.85.2....9.1....4.263..1.5.....1.1..4.9..2..61.8...']
                ]

if __name__ == "__main__":
    # uncomment to run test cases
    #processTestCases(validTestCases)
    #processTestCases(invalidTestCases)

    main()
