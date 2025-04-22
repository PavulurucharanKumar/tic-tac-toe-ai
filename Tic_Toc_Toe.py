import random
import pandas as pd
import os
from datetime import datetime

# For saving game history
CSV_FILE = "tic_tac_toe_history.csv"

def print_board(board):
    print("\n<---><---><--->\n")
    print("    0    1    2")
    for i, row in enumerate(board):
        print(i, "   | ".join(row))
        if i < 2:
            print("    ------------")

def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def get_ai_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(empty_cells)

def save_result(mode, winner, moves):
    df_new = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Mode": mode,
        "Winner": winner,
        "Moves": moves
    }])

    if os.path.exists(CSV_FILE):
        df_old = pd.read_csv(CSV_FILE)
        df_new = pd.concat([df_old, df_new], ignore_index=True)

    df_new.to_csv(CSV_FILE, index=False)
    print(f"\n✅ Game result saved to {CSV_FILE}\n")

def view_scoreboard():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        print("\n🧾 --- Game History (Last 10) ---\n")
        print(df.tail(10))
    else:
        print("No game history found.\n")

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    moves = 0

    mode = input("🎮 Select mode:\n1. Player vs Player\n2. Player vs AI\nEnter 1 or 2: ")
    print("\n")
    vs_ai = mode == "2"

    if mode == "1":
        player_x = input("Enter Player X's name: ")
        player_o = input("Enter Player O's name: ")
    else:
        player_x = input("Enter your name: ")
        player_o = "AI"

    while True:
        print_board(board)
        print(f"{player_x if current_player == 'X' else player_o}'s turn ({current_player})")

        if vs_ai and current_player == "O":
            row, col = get_ai_move(board)
            print(f"AI chose: {row}, {col}")
        else:
            try:
                row_col = input("Enter row and column (e.g., 0,1): ").split(",")
                if len(row_col) != 2:
                    raise ValueError
                row, col = map(int, row_col)
            except ValueError:
                print("❌ Invalid input. Try again.")
                continue

        if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
            board[row][col] = current_player
            moves += 1

            if check_win(board, current_player):
                print_board(board)
                winner = player_x if current_player == "X" else player_o
                print(f"🏆 {winner} wins!")
                save_result("PvAI" if vs_ai else "PvP", winner, moves)
                break

            elif is_full(board):
                print_board(board)
                print("🤝 It's a draw!")
                save_result("PvAI" if vs_ai else "PvP", "Draw", moves)
                break

            current_player = "O" if current_player == "X" else "X"
        else:
            print("⚠️ Invalid move. Try again.")

# Launcher
def main():
    while True:
        choice = input("\n=== Tic Tac Toe Menu ===\n1. Play Game\n2. View Scoreboard\n3. Exit\nChoose an option (1/2/3): ")
        if choice == "1":
            tic_tac_toe()
        elif choice == "2":
            view_scoreboard()
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please try again.")

# Run main loop
main()
