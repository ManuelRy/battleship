import pygame
import sys

# Constants
GRID_SIZE = 10
CELL_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHIP_SIZES = [1, 2, 3, 4]  # Example ship sizes

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(((GRID_SIZE + 1) * CELL_SIZE, (GRID_SIZE + 3) * CELL_SIZE))
pygame.display.set_caption('Battleship')

# Load images
ship_img = pygame.image.load('./img/ship.png')
hit_img = pygame.image.load('./img/hit.png')
miss_img = pygame.image.load('./img/miss.png')
ship_img = pygame.transform.scale(ship_img, (CELL_SIZE, CELL_SIZE))
hit_img = pygame.transform.scale(hit_img, (CELL_SIZE, CELL_SIZE))
miss_img = pygame.transform.scale(miss_img, (CELL_SIZE, CELL_SIZE))

# Function to initialize a grid
def initialize_grid():
    return [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Function to draw the grid
def draw_grid(grid, reveal_ships=False):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    
    # Draw labels
    for i in range(GRID_SIZE):
        label = font.render(str(i + 1), True, BLACK)
        screen.blit(label, (CELL_SIZE // 4, (i + 1) * CELL_SIZE + CELL_SIZE // 4))
        screen.blit(label, ((i + 1) * CELL_SIZE + CELL_SIZE // 4, CELL_SIZE // 4))
    
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            cell = grid[y][x]
            if cell == 'S' and not reveal_ships:
                text = '.'
                text_surface = font.render(text, True, BLACK)
                screen.blit(text_surface, ((x + 1) * CELL_SIZE + 10, (y + 1) * CELL_SIZE + 5))
            elif cell == 'S':
                screen.blit(ship_img, ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE))
            elif cell == 'X':
                screen.blit(hit_img, ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE))
            elif cell == 'O':
                screen.blit(miss_img, ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE))
            else:
                text = '.'
                text_surface = font.render(text, True, BLACK)
                screen.blit(text_surface, ((x + 1) * CELL_SIZE + 10, (y + 1) * CELL_SIZE + 5))

# Function to place ships on the grid
def place_ships(grid, ship_sizes):
    for ship_size in ship_sizes:
        while True:
            try:
                x = int(input(f"Enter x-coordinate for a ship of size {ship_size} (1-10): ")) - 1
                y = int(input(f"Enter y-coordinate for a ship of size {ship_size} (1-10): ")) - 1
                direction = input("Enter direction (h for horizontal, v for vertical): ").lower()
                
                if direction == 'h':
                    if x + ship_size <= GRID_SIZE and all(grid[y][x + i] == '.' for i in range(ship_size)):
                        for i in range(ship_size):
                            grid[y][x + i] = 'S'
                        break
                    else:
                        print("Invalid position or overlap! Try again.")
                
                elif direction == 'v':
                    if y + ship_size <= GRID_SIZE and all(grid[y + i][x] == '.' for i in range(ship_size)):
                        for i in range(ship_size):
                            grid[y + i][x] = 'S'
                        break
                    else:
                        print("Invalid position or overlap! Try again.")
                
                else:
                    print("Invalid direction! Please enter 'h' for horizontal or 'v' for vertical.")
            
            except (ValueError, IndexError):
                print("Invalid input! Please enter valid coordinates and direction.")

# Function to fire at opponent's grid
def fire(grid, x, y):
    if grid[y][x] == 'S':
        grid[y][x] = 'X'
        print("Hit!")
    else:
        grid[y][x] = 'O'
        print("Miss!")

# Function to check if all ships have been hit
def check_win_condition(grid):
    for row in grid:
        if 'S' in row:
            return False
    return True

# Function to display the current player's turn
def display_turn(current_player):
    font = pygame.font.Font(None, 36)
    turn_text = f"Player {current_player}'s Turn"
    text_surface = font.render(turn_text, True, BLACK)
    text_rect = text_surface.get_rect(center=((GRID_SIZE + 1) * CELL_SIZE // 2, (GRID_SIZE + 1.5) * CELL_SIZE))
    screen.blit(text_surface, text_rect)

# Main function
def main():
    num_ships = len(SHIP_SIZES)

    print("Player 1, place your ships:")
    player1_grid = initialize_grid()
    place_ships(player1_grid, SHIP_SIZES)

    print("Player 2, place your ships:")
    player2_grid = initialize_grid()
    place_ships(player2_grid, SHIP_SIZES)

    # Main game loop
    current_player = 1
    last_printed_turn = None  # To track when the player's turn changes
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x = (x // CELL_SIZE) - 1
                grid_y = (y // CELL_SIZE) - 1
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    if current_player == 1:
                        fire(player2_grid, grid_x, grid_y)
                        if check_win_condition(player2_grid):
                            draw_grid(player1_grid, reveal_ships=True)
                            display_turn(current_player)
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            print("Player 1 wins!")
                            pygame.quit()
                            sys.exit()
                        current_player = 2
                    else:           
                        fire(player1_grid, grid_x, grid_y)
                        if check_win_condition(player1_grid):
                            draw_grid(player2_grid, reveal_ships=True)
                            display_turn(current_player)
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            print("Player 2 wins!")
                            pygame.quit()
                            sys.exit()
                        current_player = 1

        screen.fill(WHITE)
        opponent_grid = player2_grid if current_player == 1 else player1_grid
        draw_grid(opponent_grid)
        display_turn(current_player)
        pygame.display.flip()

# Start the game
if __name__ == "__main__":
    main()
