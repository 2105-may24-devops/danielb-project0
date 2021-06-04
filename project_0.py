from blessed import Terminal
from pathlib import Path
import json

class ChessPiece:

    def __init__(self, player, type, first_move = False):
        self.player = player
        self.type = type

        # whether the piece has ever been moved (used for pawns)
        self.first_move = first_move
    
class Board:
    
    def __init__(self):
        # list comprehension that creates a list of lists to make a 2d board
        self.board_array = [ [ChessPiece(0, "space") for _ in range(8) ] for _ in range(8)]

        self.populate()

    # sets up the chess pieces on the board
    def populate(self):
        for i in range(8):
            self.board_array[i][1] = ChessPiece(1, "pawn")
            self.board_array[i][6] = ChessPiece(2, "pawn")

        self.board_array[0][0] = ChessPiece(1, "rook")
        self.board_array[7][0] = ChessPiece(1, "rook")
        self.board_array[0][7] = ChessPiece(2, "rook")
        self.board_array[7][7] = ChessPiece(2, "rook")

        self.board_array[1][0] = ChessPiece(1, "knight")
        self.board_array[6][0] = ChessPiece(1, "knight")
        self.board_array[1][7] = ChessPiece(2, "knight")
        self.board_array[6][7] = ChessPiece(2, "knight")

        self.board_array[2][0] = ChessPiece(1, "bishop")
        self.board_array[5][0] = ChessPiece(1, "bishop")
        self.board_array[2][7] = ChessPiece(2, "bishop")
        self.board_array[5][7] = ChessPiece(2, "bishop")

        self.board_array[3][0] = ChessPiece(1, "queen")
        self.board_array[3][7] = ChessPiece(2, "queen")

        # king
        self.board_array[4][0] = ChessPiece(1, "x")
        self.board_array[4][7] = ChessPiece(2, "x")

    # print out the current state of the board
    def show_board(self):
        print("   a  b  c  d  e  f  g  h\n")
        for y in reversed(range(len(self.board_array))):
            print(y + 1, end='  ')
            for x in range(len(self.board_array[y])):
                if self.board_array[x][y].player == 1:
                    print(self.board_array[x][y].type.upper()[0], end='  ')
                else:
                    print(self.board_array[x][y].type.lower()[0], end='  ')
            print(y + 1, end='')
            print("\n")
        print("   a  b  c  d  e  f  g  h")

    def move_piece(self, start_location, end_location, player):
        # if there is a piece at the start location that belongs to the player
        if self.board_array[int(start_location[0])][int(start_location[1])].player == player:
            print("You have a piece here")
        else:
            print("You don't have a piece here")
            return

        self.board_array[int(end_location[0])][int(end_location[1])] = self.board_array[int(start_location[0])][int(start_location[1])]
        self.board_array[int(start_location[0])][int(start_location[1])] = ChessPiece(0, "space")


def convert_position_to_index(position):
    letter_to_index = {letter: num for letter, num in zip('abcdefgh', range(8))}
    # raise Exception("Invalid position")
    index = str(letter_to_index[position[0]]) + str((int(position[1]) - 1))
    return index


# converts a move command to two board array indices
def parse_move(inputMove):
    return [convert_position_to_index(pos) for pos in inputMove.split(" to ")]

def main():
    # blessed terminal
    term = Terminal()

    my_path = Path.cwd() / "danielb-project0"

    moveHistory = []
    saveDictionary = {}

    whose_turn = 1

    my_board = Board()

    print("Welcome to Chess\n")
    option = input("Enter 1 to start new game, Enter 2 to load a saved game\n")

    # load a game
    if option == "2":
        with open(my_path / "saved_game.json") as infile:
            saveDictionary = json.load(infile)
        moveHistory = saveDictionary["moveHistory"]
        for i in moveHistory:
            parsed_moves = parse_move(i)
            my_board.move_piece(parsed_moves[0], parsed_moves[1], whose_turn)
            # update whose turn it is
            if whose_turn == 1:
                whose_turn = 2
            else:
                whose_turn = 1


    my_board.show_board()

    while True:
        print("\nIt is player " + str(whose_turn) + "'s turn")
        inputMove = input("Enter your move. (Example: a1 to a3) Or enter option for options\n")
        if inputMove == "option":
            option = input("Enter an option: history, save\n")
            if option == "history":
                for i in moveHistory:
                    print(i)
            if option == "save":
                saveDictionary = {}
                saveDictionary["moveHistory"] = moveHistory
                with open(my_path / "saved_game.json", "w") as outfile:
                    json.dump(saveDictionary, outfile, indent=4)
            continue

        parsed_moves = parse_move(inputMove)
        moveHistory.append(inputMove)

        my_board.move_piece(parsed_moves[0], parsed_moves[1], whose_turn)
        my_board.show_board()

        # update whose turn it is
        if whose_turn == 1:
            whose_turn = 2
        else:
            whose_turn = 1


    pass

main()