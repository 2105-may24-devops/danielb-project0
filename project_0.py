from blessed import Terminal
from pathlib import Path
import json

class chessPiece:

    def __init__(self, player, type, firstMove = False):
        self.player = player
        self.type = type

        # whether the piece has ever been moved (used for pawns)
        self.firstMove = firstMove
    
class board:
    
    def __init__(self):
        # list comprehension that creates a list of lists to make a 2d board
        self.boardArray = [ [chessPiece(0, "space") for _ in range(8) ] for _ in range(8)]

        self.populate()

    # sets up the chess pieces on the board
    def populate(self):
        for i in range(8):
            self.boardArray[i][1] = chessPiece(1, "pawn")
            self.boardArray[i][6] = chessPiece(2, "pawn")

        self.boardArray[0][0] = chessPiece(1, "rook")
        self.boardArray[7][0] = chessPiece(1, "rook")
        self.boardArray[0][7] = chessPiece(2, "rook")
        self.boardArray[7][7] = chessPiece(2, "rook")

        self.boardArray[1][0] = chessPiece(1, "knight")
        self.boardArray[6][0] = chessPiece(1, "knight")
        self.boardArray[1][7] = chessPiece(2, "knight")
        self.boardArray[6][7] = chessPiece(2, "knight")

        self.boardArray[2][0] = chessPiece(1, "bishop")
        self.boardArray[5][0] = chessPiece(1, "bishop")
        self.boardArray[2][7] = chessPiece(2, "bishop")
        self.boardArray[5][7] = chessPiece(2, "bishop")

        self.boardArray[3][0] = chessPiece(1, "queen")
        self.boardArray[3][7] = chessPiece(2, "queen")

        # king
        self.boardArray[4][0] = chessPiece(1, "x")
        self.boardArray[4][7] = chessPiece(2, "x")

    # print out the current state of the board
    def showBoard(self):
        print("   a  b  c  d  e  f  g  h\n")
        for y in reversed(range(len(self.boardArray))):
            print(y + 1, end='  ')
            for x in range(len(self.boardArray[y])):
                if self.boardArray[x][y].player == 1:
                    print(self.boardArray[x][y].type.upper()[0], end='  ')
                else:
                    print(self.boardArray[x][y].type.lower()[0], end='  ')
            print(y + 1, end='')
            print("\n")
        print("   a  b  c  d  e  f  g  h")

    def movePiece(self, startLocation, endLocation, player):
        # if there is a piece at the start location that belongs to the player
        if self.boardArray[int(startLocation[0])][int(startLocation[1])].player == player:
            print("You have a piece here")
        else:
            print("You don't have a piece here")
            return

        self.boardArray[int(endLocation[0])][int(endLocation[1])] = self.boardArray[int(startLocation[0])][int(startLocation[1])]
        self.boardArray[int(startLocation[0])][int(startLocation[1])] = chessPiece(0, "space")


def convertPositionToIndex(position):
    letter_to_index = {letter: num for letter, num in zip('abcdefgh', range(8))}
    # raise Exception("Invalid position")
    index = str(letter_to_index[position[0]]) + str((int(position[1]) - 1))
    return index


# converts a move command to two board array indices
def parseMove(inputMove):
    return [convertPositionToIndex(pos) for pos in inputMove.split(" to ")]

def main():
    # blessed terminal
    term = Terminal()

    myPath = Path.cwd() / "danielb-project0"

    moveHistory = []
    saveDictionary = {}

    whoseTurn = 1

    myBoard = board()

    print("Welcome to Chess\n")
    option = input("Enter 1 to start new game, Enter 2 to load a saved game\n")

    # load a game
    if option == "2":
        with open(myPath / "saved_game.json") as infile:
            saveDictionary = json.load(infile)
        moveHistory = saveDictionary["moveHistory"]
        for i in moveHistory:
            parsedMoves = parseMove(i)
            myBoard.movePiece(parsedMoves[0], parsedMoves[1], whoseTurn)
            # update whose turn it is
            if whoseTurn == 1:
                whoseTurn = 2
            else:
                whoseTurn = 1


    myBoard.showBoard()

    while True:
        print("\nIt is player " + str(whoseTurn) + "'s turn")
        inputMove = input("Enter your move. (Example: a1 to a3) Or enter option for options\n")
        if inputMove == "option":
            option = input("Enter an option: history, save\n")
            if option == "history":
                for i in moveHistory:
                    print(i)
            if option == "save":
                saveDictionary = {}
                saveDictionary["moveHistory"] = moveHistory
                with open(myPath / "saved_game.json", "w") as outfile:
                    json.dump(saveDictionary, outfile, indent=4)
            continue

        parsedMoves = parseMove(inputMove)
        moveHistory.append(inputMove)

        myBoard.movePiece(parsedMoves[0], parsedMoves[1], whoseTurn)
        myBoard.showBoard()

        # update whose turn it is
        if whoseTurn == 1:
            whoseTurn = 2
        else:
            whoseTurn = 1


    pass

main()