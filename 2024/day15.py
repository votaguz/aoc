import pygame
from pygame.locals import QUIT
import sys
import sys
import unittest
from pathlib import Path

# Add the ../ directory to the Python path
aoc_root_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(aoc_root_path))

from aoc import read_strings_by_separator, move_console_cursor_up


def gps(rows: int, columns: int) -> int:
    return rows * 100 + columns


def get_robot(board):
    _robot = '@'
    for y, row in enumerate(board):
        x = row.find(_robot)
        if x != -1:
            return x, y


def get_ahead(pos, direction):
    ahead = None
    if direction == '^':
        ahead = (pos[0], pos[1] - 1)
    elif direction == 'v':
        ahead = (pos[0], pos[1] + 1)
    elif direction == '<':
        ahead = (pos[0] - 1, pos[1])
    elif direction == '>':
        ahead = (pos[0] + 1, pos[1])
    return ahead


def move_robot(direction, robot, boxes, walls):
    ahead = get_ahead(robot, direction)
    if ahead in walls:
        return robot, boxes

    if ahead in boxes:
        moved, boxes = push_boxes(direction, ahead, boxes, walls)
        if moved:
            return ahead, boxes
        return robot, boxes

    return ahead, boxes


def push_box(direction, box, boxes, walls):
    ahead = get_ahead(box, direction)
    if ahead in walls or ahead in boxes:
        return False, boxes
    boxes.remove(box)
    boxes.add(ahead)
    return True, boxes

def find_consecutive_boxes(direction, first_box, boxes):
    consecutive_boxes = [first_box]
    ahead = get_ahead(first_box, direction)
    while ahead in boxes:
        consecutive_boxes.append(ahead)
        ahead = get_ahead(ahead, direction)
    return consecutive_boxes


def push_boxes(direction, first_box, boxes, walls):
    moved = False
    # Find all the consecutive boxes ahead of the first box
    consecutive_boxes = find_consecutive_boxes(direction, first_box, boxes)
    # reverse consecutive boxes
    while len(consecutive_boxes) > 0:
        box = consecutive_boxes.pop()
        moved, boxes = push_box(direction, box, boxes, walls)
    return moved, boxes


def get_walls(board):
    _wall = "#"
    return get_items(board, _wall)


def get_boxes(board):
    _box = "O"
    return get_items(board, _box)


def get_items(board, item):
    coordinates = set()
    for y, row in enumerate(board):
        x = row.find(item, 0)
        while x != -1 and x < len(row):
            if x != -1:
                coordinates.add((x, y))
            x = row.find(item, x + 1)
    return coordinates


def load_file(file_path, enhance=False):
    input = read_strings_by_separator(file_path, "\n\n", stripped=False)
    board = input[0].split("\n")
    directions = input[1].replace('\n', '')

    if enhance:
        enhanced_board = []
        replacements = {
            '#': '##',
            'O': '[]',
            '@': '@.',
            '.': '..'
        }


        for (row,board_row) in enumerate(board):
            # if there's no row yet, create one
            if len(enhanced_board) <= row:
                enhanced_board.append('')
            for char in board_row:
                if char == 'O':
                    print('Stop here for the box!')
                enhanced_board[row] += replacements.get(char)
        return enhanced_board, directions

    return board, directions


def print_board(robot, boxes, walls, delay=0):
    # given the walls, return the width and height of the board
    width = max([x for x, y in walls]) + 1
    height = max([y for x, y in walls]) + 1

    # initialize the board with empty spaces
    board = [['.' for _ in range(width)] for _ in range(height)]

    # place the robot on the board
    x, y = robot
    board[y][x] = '@'

    # place the boxes on the board
    for x, y in boxes:
        board[y][x] = 'O'

    # place the walls on the board
    for x, y in walls:
        board[y][x] = '#'

    # print the board
    for row in board:
        print(''.join(row))

    move_console_cursor_up(len(board), delay)


def part_one(board, directions, print_delay=0):
    robot = get_robot(board)
    boxes = get_boxes(board)
    walls = get_walls(board)

    # print_board([1,2], [], walls)

    for direction in directions:
        # print(direction)
        robot, boxes = move_robot(direction, robot, boxes, walls)
        if robot is None:
            print('Robot is None')
        print_board(robot, boxes, walls, print_delay)
        # print()

    print("\n" * (max([y for x, y in walls]) + 1))
    s = [gps(box[1], box[0]) for box in boxes]
    return sum(s)


def part_two(board, directions):
    robot = get_robot(board)
    boxes = get_boxes(board)
    walls = (get_walls(board))

    pass

# Initialize the pygame window
def initialize_window(width, height, scale=16):
    pygame.init()
    window_width = width * scale
    window_height = height * scale
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Robot Puzzle Game")
    return screen, scale


# Render the board on the pygame surface
def render_board(robot, boxes, walls, screen, scale):
    # Colors for the elements
    COLORS = {
        "background": (255, 255, 255),
        "robot": (0, 0, 255),
        "box": (255, 165, 0),
        "wall": (128, 128, 128)
    }

    # Clear the screen
    screen.fill(COLORS["background"])

    # Draw walls
    for x, y in walls:
        pygame.draw.rect(
            screen,
            COLORS["wall"],
            pygame.Rect(x * scale, y * scale, scale, scale)
        )

    # Draw boxes
    for x, y in boxes:
        pygame.draw.rect(
            screen,
            COLORS["box"],
            pygame.Rect(x * scale, y * scale, scale, scale)
        )

    # Draw robot
    x, y = robot
    pygame.draw.rect(
        screen,
        COLORS["robot"],
        pygame.Rect(x * scale, y * scale, scale, scale)
    )

    # Update the display
    pygame.display.flip()


# Main game loop for rendering
def part_one_with_rendering(board, directions, delay=0):
    robot = get_robot(board)
    boxes = get_boxes(board)
    walls = get_walls(board)

    # Get board dimensions
    width = max([x for x, y in walls]) + 1
    height = max([y for x, y in walls]) + 1

    # Initialize pygame window
    screen, scale = initialize_window(width, height)

    # Game loop
    for direction in directions:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Move robot and update state
        robot, boxes = move_robot(direction, robot, boxes, walls)

        # Render the board
        render_board(robot, boxes, walls, screen, scale)
        if delay:
            pygame.time.delay(delay)  # Add a small delay for smooth animation

    pygame.quit()

# To run the rendering version of part_one
# if __name__ == "__main__":
#     file_path = '15.txt'
#     board, directions = load_file(file_path)
#     part_one_with_rendering(board, directions)


if __name__ == "__main__":
    file_path = '15.2.test.txt'
    # board, directions = load_file(file_path)
    # print(part_one(board, directions, 0.01))
    board, directions = load_file(file_path, False)
    print(board)
    robot = get_robot(board)
    walls = get_walls(board)
    boxes = get_boxes(board)
    print_board(robot, boxes, walls, 0)
    print(part_one(board, directions, 0.01))
    # print(part_two(board, directions))


class TestDay15(unittest.TestCase):
    def test_gps(self):
        self.assertEqual(gps(1, 4), 104)

    def test_part_one(self):
        file_path = '15.test.txt'
        board, directions = load_file(file_path)
        result = part_one(board, directions)

        self.assertEqual(result, 2028)

    def test_get_walls(self):
        file_path = '15.test.txt'
        board, directions = load_file(file_path)
        robot = get_robot(board)
        boxes = get_boxes(board)
        walls = get_walls(board)
        print_board(robot, boxes, walls)

