import numpy as np
import os


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_array(self):
        return np.array([self.x, self.y])

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def dot(self, other):
        return np.dot(self.to_array(), other.to_array())

class Ship:
    def __init__(self, start_point, direction, length, number):
        self.start_point = start_point
        self.direction = direction
        self.length = length
        self.number = number

    def get_positions(self):
        return [(self.start_point.x + i * self.direction.x, self.start_point.y + i * self.direction.y) for i in range(self.length)]

class Cannon:
    def __init__(self, fire_point):
        self.fire_point = fire_point

def is_hit(fire_point, ship):
    ship_positions = ship.get_positions()
    return (fire_point.x, fire_point.y) in ship_positions

def initialize_grid(size):
    return [['.' for _ in range(size)] for _ in range(size)]

def place_ships_on_grid(grid, ships):
    for ship in ships:
        for (x, y) in ship.get_positions():
            grid[y][x] = 'S'

def display_grid(grid, hit_phase=True):
    size = len(grid)
    print("  " + " ".join(str(i) for i in range(size)))
    for i, row in enumerate(grid):
        display_row = [str(cell) if hit_phase or cell in ('X', 'O', 'S') else '.' for cell in row]
        print(f"{i} " + " ".join(display_row))
    print()

def player_place_ships(grid_size):
    ships = []
    
    ship_count = int(input("Player, enter the number of ships: "))
    for i in range(1, ship_count + 1):
        print(f"Enter coordinates for Ship {i}:")
        while True:
            try:
                x = int(input(f"Enter the x-coordinate of Ship {i}'s start point: "))
                y = int(input(f"Enter the y-coordinate of Ship {i}'s start point: "))
                if not (0 <= x < grid_size and 0 <= y < grid_size):
                    raise ValueError("Coordinates out of bounds.")
                dir_x = int(input(f"Enter the x-direction of Ship {i} (1 for right, -1 for left, 0 for no horizontal movement): "))
                dir_y = int(input(f"Enter the y-direction of Ship {i} (1 for up, -1 for down, 0 for no vertical movement): "))
                if dir_x not in (-1, 0, 1) or dir_y not in (-1, 0, 1):
                    raise ValueError("Invalid direction.")
                length = int(input(f"Enter the length of Ship {i}: "))
                if length <= 0:
                    raise ValueError("Length must be a positive integer.")
                end_x = x + (length - 1) * dir_x
                end_y = y + (length - 1) * dir_y
                if not (0 <= end_x < grid_size and 0 <= end_y < grid_size):
                    raise ValueError("Ship goes out of bounds.")
                ships.append(Ship(Vector(x, y), Vector(dir_x, dir_y), length, i))
                break
            except ValueError as ve:
                print(f"Error: {ve}")
    return ships

def player_fire(grid_size):
    while True:
        try:
            x = int(input("Enter the x-coordinate of your fire point: "))
            y = int(input("Enter the y-coordinate of your fire point: "))
            if not (0 <= x < grid_size and 0 <= y < grid_size):
                raise ValueError("Coordinates out of bounds.")
            return Vector(x, y)
        except ValueError as ve:
            print(f"Error: {ve}")

def update_grid(grid, fire_point, hit):
    if hit:
        grid[fire_point.y][fire_point.x] = 'X'
    else:
        grid[fire_point.y][fire_point.x] = 'O'

def are_all_ships_sunk(grid):
    for row in grid:
        for cell in row:
            if cell == 'S':
                return False
    return True

def display_final_grids(player1_grid, player2_grid):
    print("Player 1's final grid:")
    display_grid(player1_grid, hit_phase=False)
    print("Player 2's final grid:")
    display_grid(player2_grid, hit_phase=False)

# Main game loop
grid_size = 10
player1_grid = initialize_grid(grid_size)
player2_grid = initialize_grid(grid_size)
current_player = 1  # Player 1 starts

os.system('cls' if os.name == 'nt' else 'clear')
print("--------------------------------\n  Starting Game of Battleship \n--------------------------------\n")
print("Player 1, place your ships:")
player1_ships = player_place_ships(grid_size)
place_ships_on_grid(player1_grid, player1_ships)

print("Player 2, place your ships:")
player2_ships = player_place_ships(grid_size)
place_ships_on_grid(player2_grid, player2_ships)


while True:
    if current_player == 1:
        print("Player 1's turn:")
        fire_point = player_fire(grid_size)
        hit_any_ship = False
        for ship in player2_ships:
            if is_hit(fire_point, ship):
                print(f"Hit on Player 2's ship at start point ({ship.start_point.x}, {ship.start_point.y})")
                hit_any_ship = True
                update_grid(player2_grid, fire_point, True)
                break
        if not hit_any_ship:
            print("-----------------------------\n Y O U ' V E    M I S S E D!\n-----------------------------")
            update_grid(player2_grid, fire_point, False)

        display_grid(player2_grid)
        
        # Check win condition
        if are_all_ships_sunk(player2_grid):
            print("Player 1 wins!")
            display_final_grids(player1_grid, player2_grid)
            break

        current_player = 2  # Switch to Player 2's turn

    else:
        print("Player 2's turn:")
        fire_point = player_fire(grid_size)
        hit_any_ship = False
        for ship in player1_ships:
            if is_hit(fire_point, ship):
                print(f"Hit on Player 1's ship at start point ({ship.start_point.x}, {ship.start_point.y})")
                hit_any_ship = True
                update_grid(player1_grid, fire_point, True)
                break
        if not hit_any_ship:
            print("-----------------------------\n Y O U ' V E    M I S S E D!\n-----------------------------")
            update_grid(player1_grid, fire_point, False)

        display_grid(player1_grid)
        
        # Check win condition
        if are_all_ships_sunk(player1_grid):
            print("Player 2 wins!")
            display_final_grids(player1_grid, player2_grid)
            break

        current_player = 1  # Switch to Player 1's turn