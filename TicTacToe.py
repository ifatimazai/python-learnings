
import math


class :
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.human = 'X'
        self.ai = 'O'

    def print_board(self):
        print("\n  0   1   2")
        for i in range(3):
            print(f"{i} {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}")
            if i < 2:
                print("  --+---+--")
        print()

    def available_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        return None

    def is_draw(self):
        return len(self.available_moves()) == 0 and not self.check_winner()

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    def minimax(self, depth, is_maximizing):
        winner = self.check_winner()

        if winner == self.ai:
            return 1
        elif winner == self.human:
            return -1
        elif self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in self.available_moves():
                self.board[move[0]][move[1]] = self.ai
                score = self.minimax(depth + 1, False)
                self.board[move[0]][move[1]] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in self.available_moves():
                self.board[move[0]][move[1]] = self.human
                score = self.minimax(depth + 1, True)
                self.board[move[0]][move[1]] = ' '
                best_score = min(score, best_score)
            return best_score

    def ai_move(self):
        best_score = -math.inf
        best_move = None

        for move in self.available_moves():
            self.board[move[0]][move[1]] = self.ai
            score = self.minimax(0, False)
            self.board[move[0]][move[1]] = ' '

            if score > best_score:
                best_score = score
                best_move = move

        self.board[best_move[0]][best_move[1]] = self.ai
        return best_move

    def play(self):
        print("Tic-Tac-Toe Game!")
        print("You are X, AI is O")

        while True:
            self.print_board()

            if len(self.available_moves()) == 0:
                print("Game ended in a draw!")
                break

            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))

                if not self.make_move(row, col, self.human):
                    print("Invalid move! Try again.")
                    continue
            except:
                print("Please enter valid numbers!")
                continue

            winner = self.check_winner()
            if winner:
                self.print_board()
                print(f"Player {winner} wins!")
                break

            if self.is_draw():
                self.print_board()
                print("Game ended in a draw!")
                break

            print("AI is thinking...")
            self.ai_move()

            winner = self.check_winner()
            if winner:
                self.print_board()
                print(f"Player {winner} wins!")
                break

            if self.is_draw():
                self.print_board()
                print("Game ended in a draw!")
                break


if __name__ == "__main__":
    game = TicTacToe()
    game.play()