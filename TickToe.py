# this is tick tack toe!
class Board:
    def __init__(self):
        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.xcord = 1
        self.ycord = 1
        self.try_again = True

    def moved(self, team):
        while self.try_again:
            try:
                self.xcord = int(input("What row do you want?(1-3) ")) - 2
            except ValueError:
                print("That value is not supported")
                self.try_again = True
            try:
                self.ycord = int(input("What column do you want?(1-3) ")) - 2
            except ValueError:
                print("That value is not supported")
                self.try_again = True
            try:
                if self.board[self.xcord][self.ycord] == "":
                    self.try_again = False
                else:
                    self.try_again = True
                    print("That spot is already taken")
            except IndexError:
                self.try_again = True
                print("Those numbers are not ok")
            if self.xcord >= 2 or self.xcord <= -2:
                self.try_again = True
                print("Those are not valid values")
            elif self.ycord >= 2 or self.ycord <= -2:
                self.try_again = True
                print("Those are not valid values")
            else:
                pass
        self.try_again = True
        # print(f"{self.xcord},{self.ycord}")  # prints vetted row and column selection
        if team == "O":
            self.board[self.xcord][self.ycord] = "O"
        else:
            self.board[self.xcord][self.ycord] = "X"

    def display(self):
        print_out = ""
        for a in range(3):
            for i in range(3):
                if self.board[a - 1][i - 1] != "":
                    print_out += " " + str(self.board[a - 1][i - 1])
                else:
                    print_out += " _"
            print_out = f"{a+1}" + print_out
            print(print_out)
            print_out = ""
        print("  1 2 3")

    def did_win(self):
        result_string = ""
        result_list = []
        for each in self.board:  # checks a row for win
            for every in each:
                result_string += every
            result_list.append(result_string.replace(" ", ""))
            result_string = ""
        for i in range(3):  # checks columns for win
            for each in self.board:
                result_string += each[i-1]
            result_list.append(result_string.replace(" ", ""))
            result_string = ""
        for i in range(3):
            result_string += self.board[i - 1][i - 1]
        result_list.append(result_string.replace(" ", ""))
        result_string = ""
        for i in range(3):
            result_string += self.board[2 - i][2 - i]
        result_list.append(result_string.replace(" ", ""))
        result_string = ""
        # Checks result list for a winning list
        over = ""
        for result in result_list:
            if result == "XXX":
                return "X"
            elif result == "OOO":
                return "O"
            else:
                over = "Not Over"
        if over == "Not Over":
            return "Not Over"


Loop = "Not Over"
board = Board()
turn = 0
print("Welcome to Tick Tack Toe!")
board.display()
while Loop != "X" and Loop != "O" and Loop != "none":
    turn += 1
    print("First player's turn!")
    board.moved("X")
    board.display()
    Loop = board.did_win()
    if turn < 5 and Loop == "Not Over":  # when the board is full this ends the game
        print("Second player's turn!")
        board.moved("O")
        board.display()
        Loop = board.did_win()
    else:
        Loop = board.did_win()
        if Loop == "Not Over":
            Loop = "none"
print("Game over!")
if Loop == "none":
    print("This game is a draw!")
else:
    if Loop == "X":
        print("Player 1 wins!")
    else:
        print("Player 2 wins!")
    print(f"Congratulations, The {Loop}'s Won!")
