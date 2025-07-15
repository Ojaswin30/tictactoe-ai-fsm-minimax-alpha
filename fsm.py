import time

class TicTacToeFSM:
    def __init__(self):
        self.state = 'Start'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'Player 1'

    def transition(self, event=None):
        if self.state == 'Start':
            self.initialize_game()
            self.state = 'Player 1 Turn'
        elif self.state == 'Player 1 Turn':
            position = self.get_user_move()
            start_time = time.time()
            if self.make_move(position, 'X'):
                end_time = time.time()
                self.print_move_time(start_time, end_time)
                if self.check_win():
                    self.state = 'End Game'
                    self.end_game(f"{self.current_player} wins!")
                elif self.check_draw():
                    self.state = 'End Game'
                    self.end_game("It's a draw!")
                else:
                    self.switch_player()
        elif self.state == 'Player 2 Turn':
            position = self.decide_move('O')
            start_time = time.time()
            if self.make_move(position, 'O'):
                end_time = time.time()
                self.print_move_time(start_time, end_time)
                if self.check_win():
                    self.state = 'End Game'
                    self.end_game(f"{self.current_player} wins!")
                elif self.check_draw():
                    self.state = 'End Game'
                    self.end_game("It's a draw!")
                else:
                    self.switch_player()
        elif self.state == 'End Game':
            self.reset_game()

    def initialize_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'Player 1'
        print("Game Initialized. Player 1's turn.")
        self.print_board()

    def get_user_move(self):
        while True:
            try:
                move = input("Enter your move (row and column separated by a space): ")
                x, y = map(int, move.split())
                if 0 <= x < 3 and 0 <= y < 3:
                    return (x, y)
                else:
                    print("Invalid move. Enter values between 0 and 2.")
            except ValueError:
                print("Invalid input. Please enter two numbers separated by a space.")

    def decide_move(self, symbol):
        # Basic heuristic to make a move: choose the first available spot
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    return (i, j)
        return None

    def make_move(self, position, symbol):
        if position is None:
            print("No available moves.")
            return False
        x, y = position
        if self.board[x][y] == '':
            self.board[x][y] = symbol
            print(f"{self.current_player} placed {symbol} at position {position}.")
            self.print_board()
            return True
        else:
            print("Invalid move. Try again.")
            return False

    def check_win(self):
        lines = (
            [self.board[0], self.board[1], self.board[2]],  # rows
            [[self.board[i][0] for i in range(3)], [self.board[i][1] for i in range(3)], [self.board[i][2] for i in range(3)]],  # columns
            [[self.board[i][i] for i in range(3)], [self.board[i][2-i] for i in range(3)]]  # diagonals
        )
        for line in lines:
            for cells in line:
                if cells[0] == cells[1] == cells[2] != '':
                    return True
        return False

    def check_draw(self):
        return all(cell != '' for row in self.board for cell in row)

    def end_game(self, message):
        print(message)
        self.state = 'End Game'

    def reset_game(self):
        print("Game Over. Resetting game...")
        self.state = 'Start'
        self.transition()

    def switch_player(self):
        self.current_player = 'Player 2' if self.current_player == 'Player 1' else 'Player 1'
        self.state = 'Player 2 Turn' if self.current_player == 'Player 2' else 'Player 1 Turn'
        print(f"{self.current_player}'s turn.")

    def print_board(self):
        for row in self.board:
            print('|'.join(cell if cell != '' else ' ' for cell in row))
            print("-" * 5)

    def print_move_time(self, start_time, end_time):
        move_time = end_time - start_time
        print(f"Time taken for this move: {move_time:.4f} seconds")

# Running the game
game = TicTacToeFSM()

# Simulate the game
while game.state != 'End Game':
    game.transition()
