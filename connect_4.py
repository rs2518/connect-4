#import sys
import numpy as np
#import pygame


# Create static variables
ROW_COUNT = 6
COLUMN_COUNT = 7

# Create board as a numpy array
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


# Code for gameplay
game_over = False
board = create_board()
turn = 0

while not game_over:
    # Player 1's turn
    if turn == 0:
        col = input("It's Player 1's turn! Select a number (0-6): ")
        
        # Add piece if turn is valid

    # Player 2's turn
    else:
        col = input("It's Player 2's turn! Select a number (0-6): ")
        
        # Add piece if turn is valid
    
    # Alternate to next players turn
    turn += 1
    turn = turn % 2
    
    
#board = create_board()
#print(board)