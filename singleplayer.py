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
    def __init__(self, start_point, direction, length):
        self.start_point = start_point
        self.direction = direction
        self.length = length

    def get_positions(self):
        return [(self.start_point.x + i * self.direction.x, self.start_point.y + i * self.direction.y) for i in range(self.length)]

def is_hit(fire_point, ship):
    ship_positions = ship.get_positions()
    return (fire_point.x, fire_point.y) in ship_positions

def initialize_grid(size):
    return [['.' for _ in range(size)] for _ in range(size)]

def place_ships_on_grid(grid, ships):
    for ship in ships:
        for (x, y) in ship.get_positions():
            grid[y][x] = 'S'

def display_grid(grid):
    size = len(grid)
    print("  " + " ".join(str(i) for i in range(size)))
    for i, row in enumerate(grid):
        print(f"{i} " + " ".join(row))
    print()

def player_fire():
    x = int(input("Enter the x-coordinate of your fire point: "))
    y = int(input("Enter the y-coordinate of your fire point: "))
    return Vector(x, y)

def update_grid(grid, fire_point, hit):
    if hit:
        grid[fire_point.y][fire_point.x] = 'X'
    else:
        grid[fire_point.y][fire_point.x] = 'O'

def player_place_ships():
    ships = []
    os.system('cls' if os.name == 'nt' else 'clear')
    ship_count = int(input("Enter the number of ships: "))
    for _ in range(ship_count):
        x = int(input("Enter the x-coordinate of the ship's start point: "))
        y = int(input("Enter the y-coordinate of the ship's start point: "))
        dir_x = int(input("Enter the x-direction of the ship (1 for right, -1 for left, 0 for no horizontal movement): "))
        dir_y = int(input("Enter the y-direction of the ship (1 for up, -1 for down, 0 for no vertical movement): "))
        length = int(input("Enter the length of the ship: "))
        ships.append(Ship(Vector(x, y), Vector(dir_x, dir_y), length))
    return ships

# Main game loop
grid_size = 10
player_grid = initialize_grid(grid_size)

player_ships = player_place_ships()
place_ships_on_grid(player_grid, player_ships)
display_grid(player_grid)

while True:
    fire_point = player_fire()
    hit_any_ship = False
    for ship in player_ships:
        if is_hit(fire_point, ship):
            print(f"Hit on your ship at start point ({ship.start_point.x}, {ship.start_point.y})")
            hit_any_ship = True
            update_grid(player_grid, fire_point, True)
            break
    if not hit_any_ship:
        print("-----------------------------\n Y O U ' V E    M I S S E D! \n-----------------------------")
        update_grid(player_grid, fire_point, False)
    
    print("Player Grid:")
    display_grid(player_grid)
