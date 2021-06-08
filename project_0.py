from blessed import Terminal
from pathlib import Path
import json

class ChessPiece:

    def __init__(self, player, type, first_move = False, moved_recently = False):
        self.player = player
        self.type = type

        # whether the piece has ever been moved (used for pawns)
        self.first_move = first_move

        # whether the piece made a move recently (tracking en passant for pawns)
        self.moved_recently = moved_recently
    
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

        if self.board_array[int(start_location[0])][int(start_location[1])].first_move == False:
            print("first move")
            self.board_array[int(start_location[0])][int(start_location[1])].first_move = True

        # clear moved_recently from previously moved pieces
        for x in range(8):
            for y in range(8):
                if self.board_array[x][y].moved_recently == True:
                    self.board_array[x][y].moved_recently = False

        # mark that the piece has been moved recently
        self.board_array[int(start_location[0])][int(start_location[1])].moved_recently = True

        self.board_array[int(end_location[0])][int(end_location[1])] = self.board_array[int(start_location[0])][int(start_location[1])]
        # set empty space where the chess piece used to be
        self.board_array[int(start_location[0])][int(start_location[1])] = ChessPiece(0, "space")


def convert_position_to_index(position):
    letter_to_index = {letter: num for letter, num in zip('abcdefgh', range(8))}
    # raise Exception("Invalid position")
    index = str(letter_to_index[position[0]]) + str((int(position[1]) - 1))
    return index


# converts a move command to two board array indices
def parse_move(input_move):
    return [convert_position_to_index(pos) for pos in input_move.split(" to ")]

# returns valid move positions for a given chess piece
def find_valid_moves(chess_piece, board, start_position):
    valid_moves = []
    if chess_piece.type == "pawn":
        if chess_piece.player == 1:
            # if the pawn has never been moved before
            if chess_piece.first_move == False:
                valid_moves.append((start_position[0] + str(int(start_position[1]) + 2)))

            # can move forward?
            if int(start_position[1]) + 1 < 8:
                valid_moves.append((start_position[0] + str(int(start_position[1]) + 1)))
            
                # can attack diagonally left?
                if int(start_position[0]) > 0 and board.board_array[int(start_position[0]) - 1][int(start_position[1]) + 1].type != "space":
                    valid_moves.append(str(int(start_position[0]) - 1) + str(int(start_position[1]) + 1))

                # can attack diagonally right?
                if int(start_position[0]) < 7 and board.board_array[int(start_position[0]) + 1][int(start_position[1]) + 1].type != "space":
                    valid_moves.append(str(int(start_position[0]) + 1) + str(int(start_position[1]) + 1))
            

        else:
            # if the pawn has never been moved before
            if chess_piece.first_move == False:
                valid_moves.append((start_position[0] + str(int(start_position[1]) - 2)))

            # can move forward?
            if int(start_position[1]) - 1 > 0:
                valid_moves.append((start_position[0] + str(int(start_position[1]) - 1)))

                # can attack diagonally left?
                if int(start_position[0]) > 0 and board.board_array[int(start_position[0]) - 1][int(start_position[1]) - 1].type != "space":
                    valid_moves.append(str(int(start_position[0]) - 1) + str(int(start_position[1]) - 1))

                # can attack diagonally right?
                if int(start_position[0]) < 7 and board.board_array[int(start_position[0]) + 1][int(start_position[1]) - 1].type != "space":
                    valid_moves.append(str(int(start_position[0]) + 1) + str(int(start_position[1]) - 1))


    return valid_moves



def main():
    # blessed terminal
    term = Terminal()

    my_path = Path.home() / "danielb-project0"

    move_history = []
    save_dictionary = {}

    whose_turn = 1

    my_board = Board()

    print("Welcome to Chess\n")
    option = input("Enter 1 to start new game, Enter 2 to load a saved game\n")

    # load a game
    if option == "2":
        with open(my_path / "saved_game.json") as infile:
            save_dictionary = json.load(infile)
        move_history = save_dictionary["moveHistory"]
        for i in move_history:
            parsed_moves = parse_move(i)
            print(find_valid_moves(my_board.board_array[int(parsed_moves[0][0])][int(parsed_moves[0][1])], my_board, parsed_moves[0]))
            my_board.move_piece(parsed_moves[0], parsed_moves[1], whose_turn)
            # update whose turn it is
            if whose_turn == 1:
                whose_turn = 2
            else:
                whose_turn = 1


    my_board.show_board()

    while True:
        print("\nIt is player " + str(whose_turn) + "'s turn")
        input_move = input("Enter your move. (Example: a1 to a3) Or enter option for options\n")
        if input_move == "option":
            option = input("Enter an option: history, save\n")
            if option == "history":
                for i in move_history:
                    print(i)
            if option == "save":
                save_dictionary = {}
                save_dictionary["moveHistory"] = move_history
                with open(my_path / "saved_game.json", "w") as outfile:
                    json.dump(save_dictionary, outfile, indent=4)
            continue

        parsed_moves = parse_move(input_move)

        print(find_valid_moves(my_board.board_array[int(parsed_moves[0][0])][int(parsed_moves[0][1])], my_board, parsed_moves[0]))

        move_history.append(input_move)

        my_board.move_piece(parsed_moves[0], parsed_moves[1], whose_turn)
        my_board.show_board()

        # update whose turn it is
        if whose_turn == 1:
            whose_turn = 2
        else:
            whose_turn = 1


    pass

main()