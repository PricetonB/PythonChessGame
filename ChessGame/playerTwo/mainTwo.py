import pygame
import sys
import chessClientTwo as chessClient
# Initialize Pygame
pygame.init()

#-------------------Variables and Constants-------------------

# Define Colors (R, G, B)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
TOP_LEFT_OF_BOARD_X = 100
TOP_LEFT_OF_BOARD_Y = 100
SQUARE_SIZE = 100

# Chess board hashmap (Board Map)
Board_Map = {}
Current_Potential_Moves = []
Current_Selected_Piece = None
running = True
state = "main_menu"
host_selected_color = None
host_typed_text = ""
join_typed_text = ""




#-------------------Create the game screen and clock-------------------

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game")

# Game clock (to control the frame rate)
clock = pygame.time.Clock()






#--------------------------------------------------------------------
# Load piece images from the 'sprites' folder
piece_images = {
    'whitePawn': pygame.image.load('sprites/whitePawn.png'),
    'whiteRook': pygame.image.load('sprites/whiteRook.png'),
    'whiteKnight': pygame.image.load('sprites/whiteKnight.png'),
    'whiteBishop': pygame.image.load('sprites/whiteBishop.png'),
    'whiteQueen': pygame.image.load('sprites/whiteQueen.png'),
    'whiteKing': pygame.image.load('sprites/whiteKing.png'),
    'blackPawn': pygame.image.load('sprites/blackPawn.png'),
    'blackRook': pygame.image.load('sprites/blackRook.png'),
    'blackKnight': pygame.image.load('sprites/blackKnight.png'),
    'blackBishop': pygame.image.load('sprites/blackBishop.png'),
    'blackQueen': pygame.image.load('sprites/blackQueen.png'),
    'blackKing': pygame.image.load('sprites/blackKing.png')
}

# Resize images to fit the board squares (100x100 pixels)
for key in piece_images:
    piece_images[key] = pygame.transform.scale(piece_images[key], (100, 100))

# Resize images to fit the board squares (100x100 pixels)
for key in piece_images:
    piece_images[key] = pygame.transform.scale(piece_images[key], (100, 100))





#----------------------------CREATE BOARD MAP----------------------------------------
#BOARD MAP
# SquareID: {
#     'piece': 'pawn',
#     'color': 'white',
#     'x_coordinate': 100,
#     'y_coordinate': 100
# }

def create_board_map():
    """Creates an empty board map where all squares have no piece."""
    rows = '12345678'
    cols = 'ABCDEFGH'
    global Board_Map

    for col in cols:
        for row in rows:
            square_id = col + row
            Board_Map[square_id] = {
                'piece': None,
                'color': None,
                'x_coordinate': TOP_LEFT_OF_BOARD_X + (ord(col) - 65) * 100,
                'y_coordinate': TOP_LEFT_OF_BOARD_Y + (8 - int(row)) * 100
            }

def reset_board_map():
    """Resets the board map with the starting positions of the chess pieces."""
    create_board_map()  # Reset to an empty board first

    # Define the starting positions of the pieces
    starting_positions = {
        'A1': ('rook', 'white'), 'H1': ('rook', 'white'),
        'A8': ('rook', 'black'), 'H8': ('rook', 'black'),
        'B1': ('knight', 'white'), 'G1': ('knight', 'white'),
        'B8': ('knight', 'black'), 'G8': ('knight', 'black'),
        'C1': ('bishop', 'white'), 'F1': ('bishop', 'white'),
        'C8': ('bishop', 'black'), 'F8': ('bishop', 'black'),
        'D1': ('queen', 'white'), 'E1': ('king', 'white'),
        'D8': ('queen', 'black'), 'E8': ('king', 'black'),
    }

    # Place pawns
    for col in 'ABCDEFGH':
        starting_positions[col + '2'] = ('pawn', 'white')
        starting_positions[col + '7'] = ('pawn', 'black')

    # Update the Board_Map with pieces
    for square, (piece, color) in starting_positions.items():
        Board_Map[square]['piece'] = piece
        Board_Map[square]['color'] = color





#---------------------------------------------Potential Move Logic---------------------------------------------

def pawn_potential_moves(squareID, color, potential_moves):
    col, row = squareID[0], int(squareID[1])
    if color == 'white':
        # White pawn moves forward
        # Check if the square in front is empty
        if Board_Map[f"{col}{row + 1}"]['piece'] is None:
            potential_moves.append(f"{col}{row + 1}")  # Move 1 step forward

        # Check if the square diagonally to the right is occupied by an enemy piece
        if ord('A') <= ord(col) + 1 <= ord('H'):
            if Board_Map[f"{chr(ord(col) + 1)}{row + 1}"]['piece'] is not None and Board_Map[f"{chr(ord(col) + 1)}{row + 1}"]['color'] != color:
                potential_moves.append(f"{chr(ord(col) + 1)}{row + 1}")
        
        # Check if the square diagonally to the left is occupied by an enemy piece
        if ord('A') <= ord(col) - 1 <= ord('H'):
            if Board_Map[f"{chr(ord(col) - 1)}{row + 1}"]['piece'] is not None and Board_Map[f"{chr(ord(col) - 1)}{row + 1}"]['color'] != color:
                potential_moves.append(f"{chr(ord(col) - 1)}{row + 1}")


        # If pawn is in starting position, it can move 2 steps
        if row == 2: 
            #check if the square 2 steps ahead is empty
            if Board_Map[f"{col}{row + 2}"]['piece'] is None:
                potential_moves.append(f"{col}{row + 2}")




    else:  # Black pawn
        if Board_Map[f"{col}{row - 1}"]['piece'] is None:
            potential_moves.append(f"{col}{row - 1}")  # Move 1 step forward

        # Check if the square diagonally to the right is occupied by an enemy piece
        if ord('A') <= ord(col) + 1 <= ord('H'):
            if Board_Map[f"{chr(ord(col) + 1)}{row - 1}"]['piece'] is not None and Board_Map[f"{chr(ord(col) + 1)}{row - 1}"]['color'] != color:
                potential_moves.append(f"{chr(ord(col) + 1)}{row - 1}")

        # Check if the square diagonally to the left is occupied by an enemy piece  
        if ord('A') <= ord(col) - 1 <= ord('H'):
            if Board_Map[f"{chr(ord(col) - 1)}{row - 1}"]['piece'] is not None and Board_Map[f"{chr(ord(col) - 1)}{row - 1}"]['color'] != color:
                potential_moves.append(f"{chr(ord(col) - 1)}{row - 1}")

        # If pawn is in starting position, it can move 2 steps
        if row == 7: 
            #check if the square 2 steps ahead is empty
            if Board_Map[f"{col}{row - 2}"]['piece'] is None:
                potential_moves.append(f"{col}{row - 2}")

def rook_potential_moves(squareID, color, potential_moves):
    col, row = squareID[0], int(squareID[1])
    # Moving vertically

    # Upward moves
    for i in range(1, 8):
        if row + i <= 8:
            if Board_Map[f"{col}{row + i}"]['piece'] is not None:
                # if there is a piece there and its same color then break if its different color then add to potential moves and break
                if Board_Map[f"{col}{row + i}"]['color'] == color:
                    break
                else:
                    potential_moves.append(f"{col}{row + i}")
                    break
            else:
                potential_moves.append(f"{col}{row + i}")  
        else:
            break

    # Downward moves
    for i in range(1, 8):
        if row - i >= 1:
            if Board_Map[f"{col}{row - i}"]['piece'] is not None:
                # if there is a piece there and its same color then break if its different color then add to potential moves and break
                if Board_Map[f"{col}{row - i}"]['color'] == color:
                    break
                else:
                    potential_moves.append(f"{col}{row - i}")
                    break
            else:
                potential_moves.append(f"{col}{row - i}")
        else:
            break


    # Moving horizontally

    # Right moves
    for i in range(1, 8):
        next_col = chr(ord(col) + i)
        prev_col = chr(ord(col) - i)
        if ord('A') <= ord(next_col) <= ord('H'):
            if Board_Map[f"{next_col}{row}"]['piece'] is not None:
                # if there is a piece there and its same color then break if its different color then add to potential moves and break
                if Board_Map[f"{next_col}{row}"]['color'] == color:
                    break
                else:
                    potential_moves.append(f"{next_col}{row}")
                    break
            else:
                potential_moves.append(f"{next_col}{row}")

    # Left moves
    for i in range(1, 8):
        next_col = chr(ord(col) + i)
        prev_col = chr(ord(col) - i)
        if ord('A') <= ord(prev_col) <= ord('H'):
            if Board_Map[f"{prev_col}{row}"]['piece'] is not None:
                # if there is a piece there and its same color then break if its different color then add to potential moves and break
                if Board_Map[f"{prev_col}{row}"]['color'] == color:
                    break
                else:
                    potential_moves.append(f"{prev_col}{row}")
                    break
            else:
                potential_moves.append(f"{prev_col}{row}")

def knight_potential_moves(squareID, color, potential_moves):
    col, row = squareID[0], int(squareID[1])
    #check 8 possible moves for knight if the position is valid and if there is is no piece or piece of different color add to potential moves. if piece is same color continue
    #up 2 right 1
    if row + 2 <= 8 and ord(col) + 1 <= ord('H'):
        if Board_Map[f"{chr(ord(col) + 1)}{row + 2}"]['piece'] is None or Board_Map[f"{chr(ord(col) + 1)}{row + 2}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) + 1)}{row + 2}")
    #up 2 left 1
    if row + 2 <= 8 and ord(col) - 1 >= ord('A'):
        if Board_Map[f"{chr(ord(col) - 1)}{row + 2}"]['piece'] is None or Board_Map[f"{chr(ord(col) - 1)}{row + 2}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) - 1)}{row + 2}")
    #down 2 right 1 
    if row - 2 >= 1 and ord(col) + 1 <= ord('H'):
        if Board_Map[f"{chr(ord(col) + 1)}{row - 2}"]['piece'] is None or Board_Map[f"{chr(ord(col) + 1)}{row - 2}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) + 1)}{row - 2}")
    #down 2 left 1
    if row - 2 >= 1 and ord(col) - 1 >= ord('A'):
        if Board_Map[f"{chr(ord(col) - 1)}{row - 2}"]['piece'] is None or Board_Map[f"{chr(ord(col) - 1)}{row - 2}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) - 1)}{row - 2}")
    
    #right 2 up 1
    if row + 1 <= 8 and ord(col) + 2 <= ord('H'):
        if Board_Map[f"{chr(ord(col) + 2)}{row + 1}"]['piece'] is None or Board_Map[f"{chr(ord(col) + 2)}{row + 1}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) + 2)}{row + 1}")

    #right 2 down 1
    if row - 1 >= 1 and ord(col) + 2 <= ord('H'):
        if Board_Map[f"{chr(ord(col) + 2)}{row - 1}"]['piece'] is None or Board_Map[f"{chr(ord(col) + 2)}{row - 1}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) + 2)}{row - 1}")

    #left 2 up 1
    if row + 1 <= 8 and ord(col) - 2 >= ord('A'):
        if Board_Map[f"{chr(ord(col) - 2)}{row + 1}"]['piece'] is None or Board_Map[f"{chr(ord(col) - 2)}{row + 1}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) - 2)}{row + 1}")

    #left 2 down 1
    if row - 1 >= 1 and ord(col) - 2 >= ord('A'):
        if Board_Map[f"{chr(ord(col) - 2)}{row - 1}"]['piece'] is None or Board_Map[f"{chr(ord(col) - 2)}{row - 1}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) - 2)}{row - 1}")

def bishop_potential_moves(squareID, color, potential_moves):
    col, row = squareID[0], int(squareID[1])
    # Moving diagonally

    # Upward right moves
    for i in range(1, 8):
        if row + i <= 8 and ord(col) + i <= ord('H'):
            if Board_Map[f"{chr(ord(col) + i)}{row + i}"]['piece'] is not None:
                # if there is a piece there and its same color then break if its different color then add to potential moves and break
                if Board_Map[f"{chr(ord(col) + i)}{row + i}"]['color'] == color:
                    break
                else:
                    potential_moves.append(f"{chr(ord(col) + i)}{row + i}")
                    break
            else:
                potential_moves.append(f"{chr(ord(col) + i)}{row + i}")
        else:
            break

    # Upward left moves
    for i in range(1, 8):
        if row + i <= 8 and ord(col) - i >= ord('A'):
            if Board_Map[f"{chr(ord(col) - i)}{row + i}"]['piece'] is not None:
                # if there is a piece there and its same color then break if its different color then add to potential moves and break
                if Board_Map[f"{chr(ord(col) - i)}{row + i}"]['color'] == color:
                    break
                else:
                    potential_moves.append(f"{chr(ord(col) - i)}{row + i}")
                    break
            else:
                potential_moves.append(f"{chr(ord(col) - i)}{row + i}")
        else:
            break

    # Downward right moves
    for i in range(1, 8):
        if row - i >= 1 and ord(col) + i <= ord('H'):
            if Board_Map[f"{chr(ord(col) + i)}{row - i}"]['piece'] is not None:
                # if there is a piece there and its same color then break if its different color then add to potential moves and break
                if Board_Map[f"{chr(ord(col) + i)}{row - i}"]['color'] == color:
                    break
                else:
                    potential_moves.append(f"{chr(ord(col) + i)}{row - i}")
                    break
            else:
                potential_moves.append(f"{chr(ord(col) + i)}{row - i}")
        else:
            break

    # Downward left moves   
    for i in range(1, 8):
        if row - i >= 1 and ord(col) - i >= ord('A'):
            if Board_Map[f"{chr(ord(col) - i)}{row - i}"]['piece'] is not None:
                # if there is a piece there and its same color then break if its different color then add to potential moves and break
                if Board_Map[f"{chr(ord(col) - i)}{row - i}"]['color'] == color:
                    break
                else:
                    potential_moves.append(f"{chr(ord(col) - i)}{row - i}")
                    break
            else:
                potential_moves.append(f"{chr(ord(col) - i)}{row - i}")
        else:
            break

def king_potential_moves(squareID, color, potential_moves):
    col, row = squareID[0], int(squareID[1])
    # check 8 possible moves for king if the position is valid and if there is is
    # no piece or piece of different color add to potential moves. if piece is same color continue up
    if row + 1 <= 8:
        if Board_Map[f"{col}{row + 1}"]['piece'] is None or Board_Map[f"{col}{row + 1}"]['color'] != color:
            potential_moves.append(f"{col}{row + 1}")
    #down
    if row - 1 >= 1:
        if Board_Map[f"{col}{row - 1}"]['piece'] is None or Board_Map[f"{col}{row - 1}"]['color'] != color:
            potential_moves.append(f"{col}{row - 1}")
    #right
    if ord(col) + 1 <= ord('H'):
        if Board_Map[f"{chr(ord(col) + 1)}{row}"]['piece'] is None or Board_Map[f"{chr(ord(col) + 1)}{row}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) + 1)}{row}")
    #left
    if ord(col) - 1 >= ord('A'):
        if Board_Map[f"{chr(ord(col) - 1)}{row}"]['piece'] is None or Board_Map[f"{chr(ord(col) - 1)}{row}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) - 1)}{row}")


    #diagonal moves
    #up right
    if row + 1 <= 8 and ord(col) + 1 <= ord('H'):
        if Board_Map[f"{chr(ord(col) + 1)}{row + 1}"]['piece'] is None or Board_Map[f"{chr(ord(col) + 1)}{row + 1}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) + 1)}{row + 1}")
    #up left
    if row + 1 <= 8 and ord(col) - 1 >= ord('A'):
        if Board_Map[f"{chr(ord(col) - 1)}{row + 1}"]['piece'] is None or Board_Map[f"{chr(ord(col) - 1)}{row + 1}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) - 1)}{row + 1}")
    #down right
    if row - 1 >= 1 and ord(col) + 1 <= ord('H'):
        if Board_Map[f"{chr(ord(col) + 1)}{row - 1}"]['piece'] is None or Board_Map[f"{chr(ord(col) + 1)}{row - 1}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) + 1)}{row - 1}")
    #down left
    if row - 1 >= 1 and ord(col) - 1 >= ord('A'):
        if Board_Map[f"{chr(ord(col) - 1)}{row - 1}"]['piece'] is None or Board_Map[f"{chr(ord(col) - 1)}{row - 1}"]['color'] != color:
            potential_moves.append(f"{chr(ord(col) - 1)}{row - 1}")




#---------------------------------------------GET/SET---------------------------------------------

def get_square_clicked(mouse_pos):
    """Gets the chess square (e.g., A1, B2) based on the mouse click position."""
    x, y = mouse_pos

    if chessClient.assigned_color == "black":
        y = SCREEN_HEIGHT - y

    # Check if the click is within the bounds of the chess board
    if (TOP_LEFT_OF_BOARD_X <= x < TOP_LEFT_OF_BOARD_X + 8 * SQUARE_SIZE and
        TOP_LEFT_OF_BOARD_Y <= y < TOP_LEFT_OF_BOARD_Y + 8 * SQUARE_SIZE):
        
        # Calculate the column and row clicked
        col = chr((x - TOP_LEFT_OF_BOARD_X) // SQUARE_SIZE + ord('A'))  # A to H
        row = 8 - (y - TOP_LEFT_OF_BOARD_Y) // SQUARE_SIZE  # 1 to 8 (in reverse)

        return f"{col}{row}"
    return None

# Function to get potential moves for a piece when square is clicked
def set_current_potential_moves(squareID):
    global Current_Potential_Moves
    potential_moves = []
    piece_name = Board_Map[squareID]['piece']
    color = Board_Map[squareID]['color']
    
    if piece_name == 'pawn':
        pawn_potential_moves(squareID, color, potential_moves)


    elif piece_name == 'rook':
        rook_potential_moves(squareID, color, potential_moves)

    elif piece_name == 'knight':
        knight_potential_moves(squareID, color, potential_moves)

    elif piece_name == 'bishop':
        bishop_potential_moves(squareID, color, potential_moves)

    elif piece_name == 'queen':
        rook_potential_moves(squareID, color, potential_moves)
        bishop_potential_moves(squareID, color, potential_moves)

    elif piece_name == 'king':
        king_potential_moves(squareID, color, potential_moves)



    print(f"Potential moves for {color} {piece_name} at {squareID}: {potential_moves}")
    Current_Potential_Moves = potential_moves

def set_current_selected_piece(squareID):
    global Current_Selected_Piece
    Current_Selected_Piece = squareID
    print(f"Current Selected piece: {Current_Selected_Piece}")


def update_board(move):
    #make a function that takes in a string that is two squares for example "A2A4" and moves the piece from A2 to A4
    #update the board map
    start_square = move[:2]
    end_square = move[2:]
    Board_Map[end_square]['piece'] = Board_Map[start_square]['piece']
    Board_Map[end_square]['color'] = Board_Map[start_square]['color']
    Board_Map[start_square]['piece'] = None
    Board_Map[start_square]['color'] = None
    print(f"Moved {Board_Map[end_square]['color']} {Board_Map[end_square]['piece']} from {start_square} to {end_square} due to network move.")



#---------------------------------------------Draw---------------------------------------------
    
def draw_potential_moves():
    for move in Current_Potential_Moves:
        x, y = Board_Map[move]['x_coordinate'], Board_Map[move]['y_coordinate']
        pygame.draw.circle(screen, YELLOW, (x + 50, y + 50), 10)

def draw_chess_board():
    screen.fill(BLACK)
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                square_color = GREY
            else:
                square_color = RED
            pygame.draw.rect(screen, square_color, (TOP_LEFT_OF_BOARD_X + col * 100, TOP_LEFT_OF_BOARD_Y + row * 100, 100, 100))

def draw_pieces():
    """Draws the pieces on the board based on the board map."""
    for square, data in Board_Map.items():
        piece = data['piece']
        color = data['color']
        if piece is not None:
            # Generate the key for the piece image
            piece_key = f"{color}{piece.capitalize()}"
            piece_image = piece_images.get(piece_key)
            if piece_image:
                # Draw the piece image at the specified coordinates
                #if chessClient.assigned_color == "black": flip the piece image
                if chessClient.assigned_color == "black":
                    piece_image = pygame.transform.flip(piece_image, False, True)
                    
                screen.blit(piece_image, (data['x_coordinate'], data['y_coordinate']))


#--------------------------------------------------------------------
#main menu functions

def draw_main_menu_buttons():
    screen.fill((0, 0, 0))
    #draw a button that says single player
    #draw a button that says multiplayer
    #draw a button that says exit
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50))
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50))
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50))
    #draw text on the buttons
    font = pygame.font.Font(None, 36)
    text = font.render("Single Player", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25))
    screen.blit(text, text_rect)
    text = font.render("Multiplayer", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75))
    screen.blit(text, text_rect)
    text = font.render("Exit", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 175))
    screen.blit(text, text_rect) 

def draw_multiplayer_menu_buttons():
    screen.fill((0, 0, 0))
    # Draw buttons: Host Game, Join Game, and Back
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50))
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50))
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50))
    
    # Draw text on the buttons
    font = pygame.font.Font(None, 36)
    text = font.render("Host Game", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25))
    screen.blit(text, text_rect)
    
    text = font.render("Join Game", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75))
    screen.blit(text, text_rect)
    
    text = font.render("Back", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 175))
    screen.blit(text, text_rect)

def draw_host_game_menu_buttons():
    global host_typed_text, host_selected_color
    screen.fill((0, 0, 0))
    # Draw buttons: Select Black, Select White, Back, and Start Game
    pygame.draw.rect(screen, GREY, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 300, 200, 50))  # Black
    pygame.draw.rect(screen, GREY, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 240, 200, 50))  # White
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50))  # Back
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 250, 200, 50))  # Start Game
    
    font = pygame.font.Font(None, 36)
    


    # Text for buttons
    if host_selected_color == "black":
        text = font.render("Select Black", True, YELLOW)
    else:
        text = font.render("Select Black", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 275))
    screen.blit(text, text_rect)

    if host_selected_color == "white":
        text = font.render("Select White", True, YELLOW)
    else:
        text = font.render("Select White", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 215))
    screen.blit(text, text_rect)

    text = font.render("Back", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 175))
    screen.blit(text, text_rect)

    text = font.render("Start Game", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 275))
    screen.blit(text, text_rect)

    # Game Code text
    text = font.render("Enter Game Code:", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))
    screen.blit(text, text_rect)

    # Text box for input (this part needs handling user input)
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 350, 200, 40))

    # Draw global text_input variable text in text box 
    text = font.render(host_typed_text, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 325))
    screen.blit(text, text_rect)

def draw_join_game_menu_buttons():
    global join_typed_text
    screen.fill((0, 0, 0))
    # Draw buttons: Select Black, Select White, Back, and Start Game

    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50))  # Back
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 250, 200, 50))  # Start Game
    
    font = pygame.font.Font(None, 36)
    


    # Text for buttons
    text = font.render("Back", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 175))
    screen.blit(text, text_rect)

    text = font.render("Start Game", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 275))
    screen.blit(text, text_rect)

    # Game Code text
    text = font.render("Enter Game Code:", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))
    screen.blit(text, text_rect)

    # Text box for input (this part needs handling user input)
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 350, 200, 40))

    # Draw global text_input variable text in text box 
    text = font.render(join_typed_text, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 325))
    screen.blit(text, text_rect)

def draw_waiting_on_opponent():
    font = pygame.font.Font(None, 36)
    text = font.render("Waiting for opponent to connect...", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.95))
    screen.blit(text, text_rect)

def main_menu_loop():
    global state
    global running

    draw_main_menu_buttons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x, y = mouse_pos
            if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100:
                if SCREEN_HEIGHT // 2 - 50 <= y <= SCREEN_HEIGHT // 2 + 50:
                    print("Single Player clicked")
                    state = "single_player"
                elif SCREEN_HEIGHT // 2 + 50 <= y <= SCREEN_HEIGHT // 2 + 150:
                    print("Multiplayer clicked")
                    state = "multi_player"
                elif SCREEN_HEIGHT // 2 + 150 <= y <= SCREEN_HEIGHT // 2 + 250:
                    print("Exit clicked")
                    running = False

def multiplayer_menu_loop():
    global state, running
    draw_multiplayer_menu_buttons()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100:
                if SCREEN_HEIGHT // 2 - 50 <= y <= SCREEN_HEIGHT // 2 + 50:
                    print("Host Game clicked")
                    state = "host_game"
                elif SCREEN_HEIGHT // 2 + 50 <= y <= SCREEN_HEIGHT // 2 + 150:
                    print("Join Game clicked")
                    state = "join_game"
                elif SCREEN_HEIGHT // 2 + 150 <= y <= SCREEN_HEIGHT // 2 + 250:
                    print("Back clicked")
                    state = "main_menu"

def host_game_menu_loop():
    global state, running, host_typed_text, host_selected_color
    draw_host_game_menu_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100:
                if SCREEN_HEIGHT // 2 - 300 <= y <= SCREEN_HEIGHT // 2 - 250:
                    print("Black selected")
                    host_selected_color = "black"
                    # handle black selection
                elif SCREEN_HEIGHT // 2 - 240 <= y <= SCREEN_HEIGHT // 2 - 190:
                    print("White selected")
                    host_selected_color = "white"
                    # handle white selection
                elif SCREEN_HEIGHT // 2 + 150 <= y <= SCREEN_HEIGHT // 2 + 200:
                    print("Back clicked")
                    state = "multi_player"
                elif SCREEN_HEIGHT // 2 + 250 <= y <= SCREEN_HEIGHT // 2 + 300:
                    print("Start Game clicked")
                    # ensure game code is entered and color is selected
                    if host_typed_text and host_selected_color:
                        print("Starting game...")
                        chessClient.host_connection(host_typed_text, host_selected_color)
                        chessClient.assigned_color = host_selected_color
                        state = "multiplayer_game"
                elif SCREEN_HEIGHT // 2 - 350 <= y <= SCREEN_HEIGHT // 2 - 310:
                    print("Game code input clicked")
                    state = "getting_host_input"
                    pass

def join_game_menu_loop():
    global state, running, join_typed_text
    draw_join_game_menu_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100:

                if SCREEN_HEIGHT // 2 + 150 <= y <= SCREEN_HEIGHT // 2 + 200:
                    print("Back clicked")
                    state = "multi_player"
                elif SCREEN_HEIGHT // 2 + 250 <= y <= SCREEN_HEIGHT // 2 + 300:
                    print("Start Game clicked")
                    # ensure game code is entered and color is selected
                    if join_typed_text:
                        print("Starting game...")
                        chessClient.join_hosted_connection(join_typed_text)
                        state = "multiplayer_game"
                elif SCREEN_HEIGHT // 2 - 350 <= y <= SCREEN_HEIGHT // 2 - 310:
                    print("Game code input clicked")
                    state = "getting_join_input"
                    pass






def get_input(current_text):
    global state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            # If Enter is pressed, change the state
            if event.key == pygame.K_RETURN:
                print("Enter pressed")

                if state == "getting_host_input":
                    state = "host_game"
                elif state == "getting_join_input":
                    state = "join_game"

            # Handle the backspace separately to delete characters
            elif event.key == pygame.K_BACKSPACE:
                current_text = current_text[:-1]
            else:
                # Add the new character to the string
                current_text += event.unicode
    return current_text

def get_input_loop(current_text):
    screen.fill((0, 0, 0))  # Clear screen with black
    current_text = get_input(current_text)  # Call the function to get input

    # Display typed text
    font = pygame.font.Font(None, 36)
    text = font.render(f"Enter Game Code and Press Enter: {current_text}", True, (255, 255, 255))
    screen.blit(text, (50, 50))
    pygame.display.flip()
    
    return current_text



def multiplayer_game_loop():
    global running
    global Current_Selected_Piece
    global Current_Potential_Moves
    global host_selected_color


    draw_chess_board()
    draw_pieces()
    draw_potential_moves()

    if chessClient.assigned_color == "black":
        flipped_screen = pygame.transform.flip(screen, False, True)
        screen.blit(flipped_screen, (0, 0))            
        # Event handling

    if chessClient.connected == True:
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Quit the game
            
            
            if chessClient.clients_turn == True:
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("since chess client client turn is true and click happened running the code")
                    mouse_pos = pygame.mouse.get_pos()
                    square_clicked = get_square_clicked(mouse_pos)
                    if square_clicked:
                        print(f"Square clicked: {square_clicked}")
                        #if there is no piece selected then select the piece and get potential moves
                        if Current_Selected_Piece == None and Board_Map[square_clicked]['piece'] is not None and Board_Map[square_clicked]['color'] == chessClient.assigned_color:
                            set_current_potential_moves(square_clicked)
                            set_current_selected_piece(square_clicked)
                        #if there is a piece selected then move the piece to the clicked square if its a potential move
                        else:
                            if square_clicked in Current_Potential_Moves:
                                print(f"Moving {Current_Selected_Piece} to {square_clicked}")
                                clientData = Current_Selected_Piece + square_clicked
                                Board_Map[square_clicked]['piece'] = Board_Map[Current_Selected_Piece]['piece']
                                Board_Map[square_clicked]['color'] = Board_Map[Current_Selected_Piece]['color']
                                Board_Map[Current_Selected_Piece]['piece'] = None
                                Board_Map[Current_Selected_Piece]['color'] = None
                                Current_Selected_Piece = None
                                Current_Potential_Moves = []
                                chessClient.send_outgoing_move(clientData)
                                chessClient.clients_turn = False
                                print("Move sent to network in main game loop.")
                            else:
                                #if the clicked square is not a potential move then deselect the piece
                                print(f"{square_clicked} is not a potential move for {Current_Selected_Piece}")
                                Current_Selected_Piece = None
                                Current_Potential_Moves = []
                    else:
                        print("Clicked outside the board.")
            else:
                opponentsMove = chessClient.attempt_to_receive_move()
                if opponentsMove != None:
                    update_board(opponentsMove)
                    chessClient.clients_turn = True

    else:
        draw_waiting_on_opponent()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Quit the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("not connected to opponent yet")
                continue




#--------------------------------------------------------------------

def single_player_game_loop():
    pass


#--------------------------------------------------------------------


# Main Game Loop
def main():
    # Game loop running flag


    global Current_Selected_Piece
    global Current_Potential_Moves
    global running
    global state
    global host_typed_text
    global join_typed_text


    

    # Initialize the board with pieces
    reset_board_map()






    while running:
        #print(f"state: {state}")

        chessClient.check_connection()
        if state == "main_menu":
            main_menu_loop()
        elif state == "multi_player":
            multiplayer_menu_loop()
        elif state == "single_player":
            single_player_game_loop()
        elif state == "host_game":
            host_game_menu_loop()
        elif state == "join_game":
            join_game_menu_loop()
        elif state == "multiplayer_game":   
            multiplayer_game_loop()
        elif state == "single_player_game":
            single_player_game_loop()
        elif state == "getting_host_input":
            host_typed_text = get_input_loop(host_typed_text)

        elif state == "getting_join_input":
            join_typed_text = get_input_loop(join_typed_text)
            

        # Update the screen
        pygame.display.flip()

        # Frame rate (60 FPS)
        clock.tick(60)

    # Exit the game
    chessClient.player_socket.close()
    pygame.quit()
    sys.exit()
    chessClient.sel.unregister(chessClient.player_socket)
    chessClient.player_socket.close()


#-------------------Run the game-------------------

# Run the game
if __name__ == "__main__":
    main()
