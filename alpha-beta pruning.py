import numpy as np
import time

total_time_taken = 0.0

def create_board():
    return np.zeros((3, 3), dtype=int)

def check_win(board, player):
    for row in board:
        if np.all(row == player):
            return True
    for col in board.T:
        if np.all(col == player):
            return True
    if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
        return True
    return False

def check_draw(board):
    return not np.any(board == 0)

def print_board(board):
    symbols = {0: ".", 1: "X", -1: "O"}
    for row in board:
        print(" ".join(symbols[cell] for cell in row))
    print()

def get_possible_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i, j] == 0:
                moves.append((i, j))
    return moves

def evaluate(board):
    if check_win(board, 1):
        return 1
    elif check_win(board, -1):
        return -1
    else:
        return 0

def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player, transposition_table):
    global total_time_taken
    start_time = time.time()

    board_hash = hash(board.tobytes())
    if board_hash in transposition_table:
        return transposition_table[board_hash]

    if check_win(board, 1) or check_win(board, -1) or check_draw(board):
        score = evaluate(board)
        transposition_table[board_hash] = score
        return score

    possible_moves = get_possible_moves(board)
    if maximizing_player:
        max_eval = float('-inf')
        for move in possible_moves:
            board[move] = 1
            eval = alpha_beta_pruning(board, depth + 1, alpha, beta, False, transposition_table)
            board[move] = 0
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        elapsed_time = time.time() - start_time
        total_time_taken += elapsed_time
        transposition_table[board_hash] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for move in possible_moves:
            board[move] = -1
            eval = alpha_beta_pruning(board, depth + 1, alpha, beta, True, transposition_table)
            board[move] = 0
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        elapsed_time = time.time() - start_time
        total_time_taken += elapsed_time
        transposition_table[board_hash] = min_eval
        return min_eval

def find_best_move(board, transposition_table):
    best_move = None
    best_value = float('-inf')
    possible_moves = get_possible_moves(board)

    for move in possible_moves:
        board[move] = 1
        move_value = alpha_beta_pruning(board, 0, float('-inf'), float('inf'), False, transposition_table)
        board[move] = 0
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move

def play_game():
    board = create_board()
    human_player = -1
    ai_player = 1
    transposition_table = {}

    while True:
        print_board(board)

        # Human move
        human_move = tuple(map(int, input("Enter your move (row and column): ").split()))
        if board[human_move] != 0:
            print("Invalid move. Try again.")
            continue
        board[human_move] = human_player

        if check_win(board, human_player):
            print_board(board)
            print("Human wins!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # AI move
        ai_move = find_best_move(board, transposition_table)
        if ai_move is not None:
            board[ai_move] = ai_player
            if check_win(board, ai_player):
                print_board(board)
                print("AI wins!")
                break
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
        else:
            print_board(board)
            print("It's a draw!")
            break

    global total_time_taken
    print(f"Total time taken by the AI's alpha-beta pruning: {total_time_taken:.6f} seconds")

if __name__ == "__main__":
    play_game()

