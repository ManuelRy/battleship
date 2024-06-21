import pygame
import sys

# Constants
GRID_SIZE = 10
CELL_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(((GRID_SIZE + 1) * CELL_SIZE, (GRID_SIZE + 2) * CELL_SIZE))
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

# Function to place ships on the grid (using input for simplicity, can be modified for mouse clicks)
def place_ships(grid, num_ships):
    for _ in range(num_ships):
        while True:
            try:
                x = int(input("Enter x-coordinate for the ship (1-10): ")) - 1
                y = int(input("Enter y-coordinate for the ship (1-10): ")) - 1
                direction = input("Enter direction (h for horizontal, v for vertical): ").lower()
                ship_size = int(input("Enter size for the ship: "))
                
                if direction == 'h':
                    side = input("Enter side (r for right, l for left): ").lower()
                    if side == 'r':
                        if x + ship_size <= GRID_SIZE and all(grid[y][x + i] == '.' for i in range(ship_size)):
                            for i in range(ship_size):
                                grid[y][x + i] = 'S'
                            break
                    elif side == 'l':
                        if x - ship_size >= -1 and all(grid[y][x - i] == '.' for i in range(ship_size)):
                            for i in range(ship_size):
                                grid[y][x - i] = 'S'
                            break
                    else:
                        print("Invalid side! Please enter 'r' for right or 'l' for left.")
                
                elif direction == 'v':
                    side = input("Enter side (u for up, d for down): ").lower()
                    if side == 'd':
                        if y + ship_size <= GRID_SIZE and all(grid[y + i][x] == '.' for i in range(ship_size)):
                            for i in range(ship_size):
                                grid[y + i][x] = 'S'
                            break
                    elif side == 'u':
                        if y - ship_size >= -1 and all(grid[y - i][x] == '.' for i in range(ship_size)):
                            for i in range(ship_size):
                                grid[y - i][x] = 'S'
                            break
                    else:
                        print("Invalid side! Please enter 'u' for up or 'd' for down.")
                else:
                    print("Invalid direction! Please enter 'h' for horizontal or 'v' for vertical.")
            except (ValueError, IndexError):
                print("Invalid input! Please enter valid coordinates, direction, and ship size.")
            print("Invalid coordinates or ships overlap! Try again.")

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
    screen.blit(text_surface, (CELL_SIZE, 0))

# Main function
def main():
    num_ships = int(input("Enter the number of ships each player should have: "))

    print("Player 1, place your ships:")
    player1_grid = initialize_grid()
    place_ships(player1_grid, num_ships)

    print("Player 2, place your ships:")
    player2_grid = initialize_grid()
    place_ships(player2_grid, num_ships)

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
                            print("Player 1 wins!")
                            draw_grid(player1_grid, reveal_ships=True)
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            pygame.quit()
                            sys.exit()
                        current_player = 2
                    else:           
                        fire(player1_grid, grid_x, grid_y)
                        if check_win_condition(player1_grid):
                            print("Player 2 wins!")
                            draw_grid(player2_grid, reveal_ships=True)
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            pygame.quit()
                            sys.exit()
                        current_player = 1

        screen.fill(WHITE)
        if current_player != last_printed_turn:
            print(f"Player {current_player}'s turn")
            last_printed_turn = current_player  # Update the flag
        display_turn(current_player)
        opponent_grid = player2_grid if current_player == 1 else player1_grid
        draw_grid(opponent_grid)
        pygame.display.flip()

# Start the game
if __name__ == "__main__":
    main()
