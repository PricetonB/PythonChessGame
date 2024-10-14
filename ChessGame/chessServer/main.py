import pygame
import sys

# Initialize Pygame
pygame.init()

#-------------------Variables and Constants-------------------

# Define Colors (R, G, B)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
TOP_LEFT_OF_BOARD_X = 100
TOP_LEFT_OF_BOARD_Y = 100
SQUARE_SIZE = 100

# Chess board hashmap (Board Map)
Board_Map = {}

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

#--------------------------------------------------------------------

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
                screen.blit(piece_image, (data['x_coordinate'], data['y_coordinate']))


def get_square_clicked(mouse_pos):
    """Gets the chess square (e.g., A1, B2) based on the mouse click position."""
    x, y = mouse_pos

    # Check if the click is within the bounds of the chess board
    if (TOP_LEFT_OF_BOARD_X <= x < TOP_LEFT_OF_BOARD_X + 8 * SQUARE_SIZE and
        TOP_LEFT_OF_BOARD_Y <= y < TOP_LEFT_OF_BOARD_Y + 8 * SQUARE_SIZE):
        
        # Calculate the column and row clicked
        col = chr((x - TOP_LEFT_OF_BOARD_X) // SQUARE_SIZE + ord('A'))  # A to H
        row = 8 - (y - TOP_LEFT_OF_BOARD_Y) // SQUARE_SIZE  # 1 to 8 (in reverse)

        return f"{col}{row}"
    return None




#--------------------------------------------------------------------

# Main Game Loop
def main():
    # Game loop running flag
    running = True

    # Initialize the board with pieces
    reset_board_map()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Quit the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(get_square_clicked(event.pos))


        # draw chess board
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    square_color = GREY
                else:
                    square_color = RED
                pygame.draw.rect(screen, square_color, (TOP_LEFT_OF_BOARD_X + col * 100, TOP_LEFT_OF_BOARD_Y + row * 100, 100, 100))

        # Draw the pieces on the board
        draw_pieces()

        # Update the screen
        pygame.display.flip()

        # Frame rate (60 FPS)
        clock.tick(60)

    # Exit the game
    pygame.quit()
    sys.exit()

#-------------------Run the game-------------------

# Run the game
if __name__ == "__main__":
    main()
