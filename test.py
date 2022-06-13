from sudokusolver import Solution
import time
import os


def getTestCases():
    fin = open(os.path.join(os.path.dirname(__file__), "testcases.txt"), encoding='utf-8')

    sudokuTestCases = []
    for line in fin:
        bar = line.strip()
        foo = bar.split(":")
        if foo[1] == '1':
            sudokuTestCases.append([foo[0], foo[2]])
        elif foo[1] == '0':
            sudokuTestCases.append([foo[0]])

    return sudokuTestCases

def processTestCases(sudokuTestCases):
    solution = Solution()
    counter = 0
    for test in sudokuTestCases:
        counter += 1
        # process format
        for i, board in enumerate(test):
            arr = []
            for j, s in enumerate(board):
                if j % 9 == 0:
                    arr.append([])
                arr[-1].append(s)
            test[i] = arr

        # prints input in new format
        print('Input:')
        sudokuArray = test[0]
        for row in sudokuArray:
            print(row)

        # prints solution
        print('')
        print('Solution:')
        start = time.time()
        try:
            solution.solveSudoku(sudokuArray)
            end = time.time()
            for row in sudokuArray:
                print(row)
        except Exception as e:
            end = time.time()
            print(f'No solution; {e}')

        # checks if solution matches with given solution
        try:
            givenSolution = test[1]
            print('')
            print('Matches with given solution?')
            print('Yes') if sudokuArray == givenSolution else print('No')
        except IndexError:
            pass
        
        print('')
        print(f'Runtime: {round((end - start) * 1000)} ms')
        print(f'Completed {counter}/{len(sudokuTestCases)} tests')

        # prints separation
        print('-'*50)
        print('')

def main():
    sudokuTestCases = getTestCases()
    processTestCases(sudokuTestCases)
    input('Press Enter key to exit')

if __name__ == "__main__":
    main()
