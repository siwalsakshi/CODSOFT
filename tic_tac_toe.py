from typing import List, Optional, Tuple
import math

EMPTY = ' '

class TicTacToe:
    def __init__(self):
        # board is a list of 9 cells, indexed 0..8
        self.board: List[str] = [EMPTY] * 9

    def print_board(self):
        b = self.board
        rows = [f" {b[0]} | {b[1]} | {b[2]} ",
                "---+---+---",
                f" {b[3]} | {b[4]} | {b[5]} ",
                "---+---+---",
                f" {b[6]} | {b[7]} | {b[8]} "]
        print('\n'.join(rows))

    def print_board_positions(self):
        # Helpful reference for the user (1-9)
        nums = [str(i+1) for i in range(9)]
        rows = [f" {nums[0]} | {nums[1]} | {nums[2]} ",
                "---+---+---",
                f" {nums[3]} | {nums[4]} | {nums[5]} ",
                "---+---+---",
                f" {nums[6]} | {nums[7]} | {nums[8]} "]
        print('\n'.join(rows))

    def available_moves(self) -> List[int]:
        return [i for i, cell in enumerate(self.board) if cell == EMPTY]

    def make_move(self, idx: int, player: str) -> None:
        if self.board[idx] != EMPTY:
            raise ValueError("Cell already occupied")
        self.board[idx] = player

    def undo_move(self, idx: int) -> None:
        self.board[idx] = EMPTY

    def is_full(self) -> bool:
        return all(cell != EMPTY for cell in self.board)

    def check_winner(self) -> Optional[str]:
        b = self.board
        lines = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for a,bidx,c in lines:
            if self.board[a] == self.board[bidx] == self.board[c] != EMPTY:
                return self.board[a]
        return None


def minimax(board: TicTacToe, depth: int, alpha: int, beta: int, maximizing: bool,
            ai_player: str, human_player: str) -> Tuple[int, Optional[int]]:
    """
    Returns (score, best_move_index). Scores are scaled so that quicker wins are better.
    """
    winner = board.check_winner()
    if winner == ai_player:
        return (10 - depth, None)
    elif winner == human_player:
        return (depth - 10, None)
    elif board.is_full():
        return (0, None)

    best_move: Optional[int] = None

    if maximizing:
        max_eval = -math.inf
        for move in board.available_moves():
            board.make_move(move, ai_player)
            eval_score, _ = minimax(board, depth + 1, alpha, beta, False, ai_player, human_player)
            board.undo_move(move)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return (max_eval, best_move)
    else:
        min_eval = math.inf
        for move in board.available_moves():
            board.make_move(move, human_player)
            eval_score, _ = minimax(board, depth + 1, alpha, beta, True, ai_player, human_player)
            board.undo_move(move)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return (min_eval, best_move)


def ai_move(game: TicTacToe, ai_player: str, human_player: str) -> int:
    # If the board is empty, play the corner (or center) to speed up decision
    if len(game.available_moves()) == 9:
        return 4  # choose center as a strong opening
    score, move = minimax(game, 0, -math.inf, math.inf, True, ai_player, human_player)
    assert move is not None
    return move


def human_turn(game: TicTacToe, human_player: str):
    while True:
        try:
            raw = input("Enter your move (1-9): ").strip()
            pos = int(raw) - 1
            if pos not in range(9):
                print("Invalid number. Choose 1-9.")
                continue
            if game.board[pos] != EMPTY:
                print("Cell already taken. Pick another.")
                continue
            game.make_move(pos, human_player)
            break
        except ValueError:
            print("Please enter a number from 1 to 9.")


def choose_symbol() -> Tuple[str, str]:
    while True:
        choice = input("Choose your symbol (X/O). X always goes first. [X/O]: ").strip().upper()
        if choice == 'X':
            return ('X', 'O')
        elif choice == 'O':
            return ('O', 'X')
        else:
            print("Please type X or O.")


def main():
    print("=== Tic-Tac-Toe (Unbeatable AI) ===")
    human, ai = choose_symbol()
    human_first = (human == 'X')

    game = TicTacToe()

    print("Positions are numbered like this:")
    game.print_board_positions()
    print()

    current_player_is_human = human_first

    while True:
        game.print_board()
        print()

        winner = game.check_winner()
        if winner or game.is_full():
            break

        if current_player_is_human:
            print("Your turn")
            human_turn(game, human)
        else:
            print("AI is thinking...")
            move = ai_move(game, ai, human)
            game.make_move(move, ai)
            print(f"AI played at position {move + 1}")

        current_player_is_human = not current_player_is_human
        print()

    game.print_board()
    winner = game.check_winner()
    if winner == human:
        print("Congratulations — you won! 🎉")
    elif winner == ai:
        print("AI wins. Better luck next time!")
    else:
        print("It's a draw.")


if __name__ == '__main__':
    main()
