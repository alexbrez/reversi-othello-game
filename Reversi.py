import copy

class Reversi:
    def __init__(self):
        self.board = self.create_initial_board()
        self.current_player = "X"

    def create_initial_board(self):
        board = [[' ' for _ in range(8)] for _ in range(8)]
        board[3][3], board[3][4] = 'O', 'X'
        board[4][3], board[4][4] = 'X', 'O'
        return board
    
    def print_board(self):
        print("   " + "   ".join(str(i) for i in range(8)))
        print("  " + "+---" * 8 + "+")
    
        for row in range(8):
       
            print(f"{row} | " + " | ".join(self.board[row][col] if self.board[row][col] != ' ' else ' ' for col in range(8)) + " |")
            print("  " + "+---" * 8 + "+")
        print()

    def is_valid_move(self, board, row, col, player):
        if board[row][col]!= ' ':
            return False
        

        opponent = 'O' if player == 'X' else 'X'
        valid = False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


        for dr, dc in directions:
            r, c = row + dr, col + dc
            count = 0
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                r, c = r + dr, c + dc
                count += 1
            if count > 0 and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                valid = True
                break
        return valid
    
    def make_move(self, board, row, col, player):
        opponent = 'O' if player == 'X' else 'X'
        board[row][col] = player
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr,dc in directions:
            r, c = row + dr, col + dc
            tiles_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                tiles_to_flip.append((r, c))
                r, c = r +dr, c + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                for rr, cc in tiles_to_flip:
                    board[rr][cc] = player

    def get_valid_moves(self, board, player):
        return [(r, c) for r in range(8) for c in range(8) if self.is_valid_move(board, r, c, player)]


    def evaluate_board(self, board):
        x_count = sum(row.count('X') for row in board)
        o_count = sum(row.count('O') for row in board)
        return x_count - o_count
    
    def minimax(self, board, depth, maximizing_player, alpha, beta):
        if depth == 0 or not self.get_valid_moves(board, 'X') and not self.get_valid_moves(board, 'O'):
            return self.evaluate_board(board), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_valid_moves(board, 'X'):
                new_board = copy.deepcopy(board)
                self.make_move(new_board, move[0], move[1], 'X')
                eval, _ = self.minimax(new_board, depth - 1, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_valid_moves(board, 'O'):
                new_board = copy.deepcopy(board)
                self.make_move(new_board, move[0], move[1], 'O')
                eval, _ = self.minimax(new_board, depth - 1, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
        
    def is_game_over(self):
        return not self.get_valid_moves(self.board, 'X') and not self.get_valid_moves(self.board, 'O')

    def get_user_move(self):
        while True:
            try:
                row = int(input("Give a row (0-7): "))
                col = int(input("Give a column (0-7): "))
                if (row, col) in self.get_valid_moves(self.board, 'X'):
                    return row, col
                print("Wrong move!Try again!.")
            except ValueError:
                print("Enter valid numbers for rows and columns.")

    def play(self):
        
        while not self.is_game_over():
            self.print_board()
            if self.current_player == 'X':
                row, col = self.get_user_move()
                self.make_move(self.board, row, col, 'X')
                self.current_player = 'O'
            else:
                _, move = self.minimax(self.board, 3, True, float('-inf'), float('inf'))
                if move:
                    print(f"The computer selects: {move}")
                    self.make_move(self.board, move[0], move[1], 'O')
                self.current_player = 'X'

        self.print_board()
        x_count = sum(row.count('X') for row in self.board)
        o_count = sum(row.count('O') for row in self.board)
        if x_count > o_count:
            print("The winner is X!")
        elif o_count > x_count:
            print("The winner is O!")
        else:
            print("Tie!")

if __name__ == "__main__":
    game = Reversi()
    game.play()