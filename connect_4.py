#import sys
import numpy as np
#import pygame


# Create static variables
ROW_COUNT = 6
COLUMN_COUNT = 7

# Create board as a numpy array
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


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


# Code for gameplay
game_over = False
board = create_board()
turn = 0

while not game_over:
    # Player 1's turn
    if turn == 0:
        piece = 1
        col = input("It's Player 1's turn! Select a number (0-6): ")
        
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)


    # Player 2's turn
    else:
        piece = -1
        col = input("It's Player 2's turn! Select a number (0-6): ")
        
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)
    
    # Alternate to next players turn
    turn += 1
    turn = turn % 2

    
    
#board = create_board()
#print(board)