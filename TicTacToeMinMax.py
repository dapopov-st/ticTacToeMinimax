"""This program lets a person place the first piece on a tic-tac-toe board.  The computer uses the
minimax algorithm to ensure that the person never wins (a tie is possible).  The game is played
in the console and numbers for available position are displayed for the person playing.
 This feature requires the use of two auxiliary functions.  In addition, the best possible
 score and the best move are calculated in a single run of the minimax algorithm."""

import time  # will use this to introduce a pause between the person's and computer's choice

personChoices = []
computerChoices = []

gameBoard2 = [['1', '|', '2', '|', '3'],
              ['-', '+', '-', '+', '-'],
              ['4', '|', '5', '|', '6'],
              ['-', '+', '-', '+', '-'],
              ['7', '|', '8', '|', '9']]


def main(personChoices, computerChoices, gameBoard, user="person"):
    gameOver = False
    depth = 0  # no moves yet, will track how many moves forward that the computer will evaluate the board
    score = 0
    print("Here is the game board")
    printGameBoard(gameBoard)

    while not gameOver:  # Score starts with 0, so not score is true, once 10 or -10, not score will be false
        if user == "person":
            isMax = True
            makeMove(gameBoard, "person", depth, isMax)
            printGameBoard(gameBoard)
            score, _, _ = checkWinner(user, personChoices, computerChoices)
            _, winner, _ = checkWinner(user, personChoices, computerChoices)
            _, _, gameOver = checkWinner(user, personChoices, computerChoices)

            if winner != "Tie" and winner != "":
                print(winner)
            elif gameOver:
                print("Tie")
            time.sleep(1)
            user = "computer"

        elif user == "computer":
            isMax = False
            makeMove(gameBoard, "computer", depth, isMax)
            print("Computer's move: ")
            printGameBoard(gameBoard)

            score, _, _ = checkWinner(user, personChoices, computerChoices)
            _, winner, _ = checkWinner(user, personChoices, computerChoices)
            _, _, gameOver = checkWinner(user, personChoices, computerChoices)

            if winner != "Tie" and winner != "":
                print(winner)
            elif gameOver:
                print("Tie")
            user = "person"


def makeMove(board, user, depth, isMax):
    """makeMove function takes in the board, the user, depth, and isMax. isMax is true if it's
    the person's term, False otherwise.  This function requires input from the user and
    definitively places the piece, hence it's not used in minimax"""
    if user == "person":
        position = int(input("Please enter your placement 1 - 9: "))
        while (position in personChoices) or (position in computerChoices):
            print("You either did not enter an integer or the position is taken")
            position = int(input("Please enter your placement 1 - 9: "))

    elif user == "computer":
        bestMove = minimax(board, depth, isMax, personChoices, computerChoices)
        position = convertToPos(bestMove[1], bestMove[2])
        symbol = 'O'

    placePosition(position, board, user)


def placePosition(position, board, user):
    """Places the user's piece at the specified position on the board"""
    symbol = "X" if user == "person" else "O"
    # fills out the first row of of the board
    positionHelper(1, 4, 0, board, position, symbol)
    # fills out the second row of of the board
    positionHelper(4, 7, 2, board, position, symbol)
    # fills out the third row of of the board
    positionHelper(7, 10, 4, board, position, symbol)

    return board


def positionHelper(a, b, c, board, position, symbol):
    """Used in the placePosition function to avoid repetition"""
    for i in range(a, b):
        if position == i:
            board[c][2 * (i - a)] = symbol
            if symbol == 'X':
                personChoices.append(position)
            elif symbol == 'O':
                computerChoices.append(position)


def printGameBoard(board):
    """Prints the board"""
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            print(board[i][j], end=" ")
        print()


def placePieceForEval(board, user, position):
    """Places the user's piece at a specified position for evaluation in minimax"""
    symbol = "X" if user == "person" else "O"
    placePosition(position, board, user)


def convertToPos(i, j):
    """Converts board coordinates to a position 1-9 on the board"""
    positionsDict = {(0, 0): 1, (0, 2): 2, (0, 4): 3, (2, 0): 4, (2, 2): 5, (2, 4): 6, (4, 0): 7, (4, 2): 8, (4, 4): 9}
    return positionsDict[(i, j)]


def convertPosToBoard(pos):
    """Converts a position 1-9 on the board to board coordinates """
    boardDict = {1: (0, 0), 2: (0, 2), 3: (0, 4), 4: (2, 0), 5: (2, 2), 6: (2, 4), 7: (4, 0), 8: (4, 2), 9: (4, 4)}
    return boardDict[pos]


def checkWinner(user, personChoices, computerChoices):
    """Given user, personChoices, and computerChoices, checks for the winner.
    Return the score, winner (or a tie), and True if the game is over/False if not"""
    allWinning = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9],
                  [3, 5, 7]]  # list of lists of all winning positions

    for w in allWinning:
        if w[0] in personChoices and w[1] in personChoices and w[2] in personChoices:
            return 10, "Player wins", True

    for w in allWinning:
        if w[0] in computerChoices and w[1] in computerChoices and w[2] in computerChoices:
            return -10, "Computer wins", True

    if len(personChoices) + len(computerChoices) == 9:
        # print("Tie")
        return 0, "Tie", True

    return 0, "", False

def minimax(board, depth, isMax, personChoices, computerChoices):
    """The minimax algorithm evaluates all future positions, assuming that the opponent
    plays optimally.  It returns the score, and row and column of the best move"""
    user = "person" if isMax else "computer"
    score, _, _ = checkWinner(user, personChoices, computerChoices)
    if score == 10 or score == -10:
        return score, 1, 1  # come back to this and see if can fix
    if len(personChoices) + len(computerChoices) == 9:
        return 5, 0, 0

    if isMax:  # person's turn
        bestScore = -1000
        bestMoveRow = 1
        bestMoveCol = 1
        for i in range(3):
            for j in range(3):
                if board[2 * i][2 * j] != "X" and board[2 * i][2 * j] != "O":
                    position = convertToPos(2 * i, 2 * j)
                    placePieceForEval(board, user, position)
                    score, _, _ = minimax(board, depth + 1, False, personChoices, computerChoices)
                    personChoices.pop()
                    m, n = convertPosToBoard(position)
                    board[m][n] = position  # undoing the move and rewriting the num on board
                    if score > bestScore:
                        bestScore = score
                        bestMoveRow = m
                        bestMoveCol = n

        return bestScore, bestMoveRow, bestMoveCol
    else:
        bestScore = 1000
        bestMoveRow = -1
        bestMoveCol = -1
        for i in range(3):
            for j in range(3):
                if board[2 * i][2 * j] != "X" and board[2 * i][2 * j] != "O":
                    position = convertToPos(2 * i, 2 * j)
                    placePieceForEval(board, user, position)
                    score, _, _ = minimax(board, depth + 1, True, personChoices, computerChoices)
                    computerChoices.pop()
                    m, n = convertPosToBoard(position)
                    board[m][n] = position
                    if score < bestScore:
                        bestScore = score
                        bestMoveRow = m
                        bestMoveCol = n
        return bestScore, bestMoveRow, bestMoveCol


main(personChoices, computerChoices, gameBoard2)
