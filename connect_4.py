#import sys
import numpy as np
import pygame     # conda install is FAULTY. Use pip


# Create static variables
ROW_COUNT = 6
COLUMN_COUNT = 7
N_CONNECTS = 4

# Create board as a numpy array
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

# Print board in correct orientation
def print_board(board):
    print(np.flip(board, axis=0))

# Replace zero entry on board matrix with 'piece'
def drop_piece(board, row, col, piece):
    board[row, col] = piece
    
# Check if the final row of the board is available for a given column
def is_valid_location(board, col):
    if board[ROW_COUNT - 1, col] == 0:
        return True
    else:
        return False

# Get the index of the next available row (as pieces stack on top each other)
def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row, col] == 0:
            return row


# Search for winning move using 'kernel' type strategy. Define win types
def horizontal_win(kernel, piece):
    for row in range(kernel.shape[0]):
        if all(kernel[row, 0:N_CONNECTS] == np.full(N_CONNECTS, piece)):
            return True
        
def vertical_win(kernel, piece):
    for col in range(kernel.shape[1]):
        if all(kernel[0:N_CONNECTS, col] == np.full(N_CONNECTS, piece)):
            return True
        
def diagonal_win(kernel, piece):
    if (all(np.diag(kernel) == np.full(N_CONNECTS, piece)) or
        all(np.diag(np.flip(kernel, axis=1)) == np.full(N_CONNECTS, piece))):
        return True

# General winning move function
def check_wins(kernel, piece):
    if (horizontal_win(kernel, piece) or
        vertical_win(kernel, piece) or
        diagonal_win(kernel, piece)):
        return True

# Check winning move using 'sliding kernel'
def is_winning_move(board, piece):
    for col in range(board.shape[1] - N_CONNECTS):
        for row in range(board.shape[0] - N_CONNECTS):
            kernel = board[row:row+N_CONNECTS, col:col+N_CONNECTS]
            if check_wins(kernel, piece):
                return True
            
    

# Code for gameplay. Initialise variables for loop
game_over = False
board = create_board()
print_board(board)
turn = 0

while not game_over:
    # Player 1's turn
    if turn == 0:
        piece = 1
        col = int(input("It's Player 1's turn! Select a number (0-6): "))
        
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)
            
            if is_winning_move(board, piece):
                print("Player 1 wins!!!")
                game_over = True


    # Player 2's turn
    else:
        piece = -1
        col = int(input("It's Player 2's turn! Select a number (0-6): "))
        
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)
            
            if is_winning_move(board, piece):
                print("Player 2 wins!!!")
                game_over = True
                
    
    print_board(board)
    
    # Alternate to next players turn
    turn += 1
    turn = turn % 2

    
   
#board = create_board()
#print(board)



# TIMESTAMP: Video 2 @10:00
