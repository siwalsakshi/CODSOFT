board=["-","-","-",
       "-","-","-",
       "-","-","-"]
def print_board():
    for row in board:
        print(" | ".join(row))
    print()

#Return "X" if human wins, "O" if AI wins, None otherwise.
def check_winner():
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != "-":
            return row[0]
        
        