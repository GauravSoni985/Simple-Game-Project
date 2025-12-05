import os
import random
from colorama import init, Fore, Style

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    print()
    for i in range(0, 9, 3):
        row = board[i:i+3]
        print(" | ".join(row))
        if i < 6:
            print("--+---+--")
    print()

def check_win(board, player):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(all(board[i] == player for i in line) for line in wins)

def is_draw(board):
    return all(cell in ['X', 'O'] for cell in board)

def get_symbol(player_name, player_symbols):
    return player_symbols[player_name]

def color_symbol(sym):
    if sym == 'X':
        return Fore.RED + 'X' + Style.RESET_ALL
    elif sym == 'O':
        return Fore.CYAN + 'O' + Style.RESET_ALL
    else:
        return sym

def play_round(player_names, player_symbols, scores):
    board = [str(i+1) for i in range(9)]
    current = random.choice(player_names)

    while True:
        clear()
        print(f"{player_names[0]} (X) vs {player_names[1]} (O)")
        print(f"Score: {player_names[0]} - {scores[player_names[0]]}, {player_names[1]} - {scores[player_names[1]]}")
        print(f"\n🎮 {current}'s turn ({get_symbol(current, player_symbols)})")
        print_board([color_symbol(cell) for cell in board])

        move = input("Choose a position (1-9): ")
        if not move.isdigit() or not 1 <= int(move) <= 9:
            input("❌ Invalid input! Press Enter to try again.")
            continue

        move = int(move) - 1
        if board[move] in ['X', 'O']:
            input("❌ Spot already taken! Press Enter to try again.")
            continue

        board[move] = get_symbol(current, player_symbols)

        if check_win(board, get_symbol(current, player_symbols)):
            clear()
            print_board([color_symbol(cell) for cell in board])
            print(f"🎉 {current} wins!")
            scores[current] += 1
            break

        if is_draw(board):
            clear()
            print_board([color_symbol(cell) for cell in board])
            print("🤝 It's a draw!")
            break

        # Switch player
        current = player_names[0] if current == player_names[1] else player_names[1]

def main():
    clear()
    print("🎲 Welcome to Modified Tic Tac Toe!")
    p1 = input("Enter name for Player 1 (X): ") or "Player 1"
    p2 = input("Enter name for Player 2 (O): ") or "Player 2"

    player_names = [p1, p2]
    player_symbols = {p1: 'X', p2: 'O'}
    scores = {p1: 0, p2: 0}

    while True:
        play_round(player_names, player_symbols, scores)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != 'y':
            print("\n🏁 Final Scoreboard:")
            for name in player_names:
                print(f"{name}: {scores[name]} wins")
            print("Thanks for playing!")
            break

main()
