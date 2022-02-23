import sys
import numpy as np
import pygame as pg     # conda install is FAULTY. Use pip


# Create static variables
ROW_COUNT = 6
COLUMN_COUNT = 7
N_CONNECTS = 4

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PIECES = {1:RED, -1:YELLOW, 0:WHITE}    # Piece:Colour (including empty slot)
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 5)
OFFSET = int(SQUARE_SIZE/2)

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
SCREEN_RECT = ((0, 0), size)
BOARD_RECT = ((0, SQUARE_SIZE), (width, height - SQUARE_SIZE))



# =============================================================================
# UTILITIES
# =============================================================================
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


# Function for player's move
def player_move(board, col, turn):
    piece = list(PIECES.keys())[turn]
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, piece)
        
        if is_winning_move(board, piece):
            return True
        else:
            return False
            
# Draw board with pygame graphics
def draw_board(board):
    # Draw background and board
    pg.draw.rect(screen, WHITE, ((0, 0), size))
    pg.draw.rect(screen, BLUE,
                 ((0, SQUARE_SIZE), (width, height-SQUARE_SIZE)))
    
    # Draw pieces and re-render screen
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            slot = board[row][col]
            pg.draw.circle(
                screen, PIECES[slot],
                (SQUARE_SIZE*col+OFFSET, height-(SQUARE_SIZE*row+OFFSET)),
                RADIUS)
    pg.display.update()
                    

# Code for gameplay. Initialise variables for loop
game_over = False
board = create_board()
print_board(board)
turn = 0



# =============================================================================
# GAMEPLAY
# =============================================================================
# Initialise pygame
pg.init()
screen = pg.display.set_mode(size)
draw_board(board)
pg.display.update()

while not game_over:
    for event in pg.event.get():
        # Exit system when game ends
        if event.type == pg.QUIT:
            sys.exit()
        
        # Render animation for piece along top of screen
        if event.type == pg.MOUSEMOTION:
            # Stop previously rendered pieces remaining on the screen
            pg.draw.rect(screen, WHITE, ((0, 0), (width, SQUARE_SIZE)))
            
            piece = PIECES[list(PIECES.keys())[turn]]   # Player colour
            pg.draw.circle(screen, piece, (event.pos[0], OFFSET), RADIUS)
        pg.display.update()
        
        # Set event for dropping a piece (mouse click)
        if event.type == pg.MOUSEBUTTONDOWN:
            col = int(event.pos[0]//SQUARE_SIZE)
            game_over = player_move(board, col, turn)
        
            print_board(board)
            print("")
            if game_over:
                print("Player ", turn+1, " wins!!!")
            draw_board(board)
            
            # Alternate to next players turn
            turn += 1
            turn = turn % 2
            
            # Wait 3 seconds before closing game
            if game_over:
                pg.time.wait(3000)