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
    if ahead in walls:
        return False, boxes
    if ahead in boxes:
        return False, boxes
    boxes.pop(box)
    boxes[ahead] = ahead
    return True, boxes


def find_consecutive_boxes(direction, first_box, boxes):
    consecutive_boxes = [first_box]
    ahead = get_ahead(first_box, direction)
    while ahead in boxes:
        consecutive_boxes.append(boxes[ahead])
        ahead = get_ahead(boxes[ahead], direction)
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
    coordinates = {}
    for y, row in enumerate(board):
        x = row.find(item, 0)
        while x != -1 and x < len(row):
            if x != -1:
                coordinates[(x, y)] = (x, y)
            x = row.find(item, x + 1)
    return coordinates


def load_file(file_path):
    input = read_strings_by_separator(file_path, "\n\n", stripped=False)
    board = input[0].split("\n")
    directions = input[1].replace('\n', '')

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
    pass


class TestDay15(unittest.TestCase):
    def test_gps(self):
        self.assertEqual(gps(1, 4), 104)

    def test_part_one(self):
        file_path = '15.txt'
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


if __name__ == "__main__":
    file_path = '15.txt'
    board, directions = load_file(file_path)
    print(part_one(board, directions, 0))
    print(part_two(board, directions))
