
import unittest

from .generator import MazeGenerator
from .maze import Maze, EAST, NORTH
from .validator import (
    count_passages,
    get_accessible_neighbours,
    has_open_3x3,
    is_connected,
    is_perfect,
    validate_non_perfect,
    validate_walls,
)


ALGORITHMS = ("dfs", "origin_shift")


def count_real_dead_ends(maze: Maze) -> int:
    """Count dead ends that could gain another passage."""
    directions = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0),
    ]

    count = 0

    for y in range(maze.height):
        for x in range(maze.width):
            if (x, y) in maze.blocked:
                continue

            neighbours = get_accessible_neighbours(
                maze, (x, y)
            )

            if len(neighbours) != 1:
                continue

            # Does this dead end have another
            # walkable adjacent cell?
            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if (
                    0 <= nx < maze.width
                    and 0 <= ny < maze.height
                    and (nx, ny) not in maze.blocked
                    and (nx, ny) not in neighbours
                ):
                    count += 1
                    break

    return count


class TestMazeGenerator(unittest.TestCase):

    def test_perfect_maze(self):
        """Both algorithms produce valid perfect mazes."""
        for algorithm in ALGORITHMS:
            for width, height in [
                (2, 2),
                (5, 5),
                (10, 10),
                (15, 12),
                (20, 15),
            ]:
                with self.subTest(
                    algorithm=algorithm,
                    size=(width, height),
                ):
                    maze = MazeGenerator(
                        width, height, seed=42
                    ).generate(
                        algorithm=algorithm,
                        perfect=True,
                    )

                    self.assertTrue(validate_walls(maze))
                    self.assertTrue(is_connected(maze))
                    self.assertTrue(is_perfect(maze))
                    self.assertFalse(has_open_3x3(maze))

                    walkable = (
                        width * height - len(maze.blocked)
                    )

                    self.assertEqual(
                        count_passages(maze),
                        walkable - 1,
                    )

    def test_non_perfect_maze(self):
        """Non-perfect mazes satisfy Pac-Man requirements."""
        for algorithm in ALGORITHMS:
            for width, height in [
                (9, 7),
                (10, 10),
                (15, 12),
                (20, 15),
            ]:
                for seed in range(10):
                    with self.subTest(
                        algorithm=algorithm,
                        size=(width, height),
                        seed=seed,
                    ):
                        maze = MazeGenerator(
                            width, height, seed=seed
                        ).generate(
                            algorithm=algorithm,
                            perfect=False,
                        )

                        self.assertTrue(
                            validate_walls(maze)
                        )
                        self.assertTrue(is_connected(maze))
                        self.assertFalse(
                            has_open_3x3(maze)
                        )
                        self.assertTrue(
                            validate_non_perfect(maze)
                        )

                        walkable = (
                            width * height
                            - len(maze.blocked)
                        )

                        cycles = (
                            count_passages(maze)
                            - walkable + 1
                        )

                        self.assertGreaterEqual(cycles, 2)

                        # Bonus: zero REAL dead ends
                        self.assertEqual(
                            count_real_dead_ends(maze), 0
                        )

    def test_small_maze_omits_pattern(self):
        """Small mazes omit the 42 pattern."""
        for width, height in [
            (2, 2),
            (5, 5),
            (8, 8),
            (9, 6),
        ]:
            with self.subTest(size=(width, height)):
                maze = MazeGenerator(
                    width, height, seed=42
                ).generate(perfect=True)

                self.assertEqual(len(maze.blocked), 0)
                self.assertTrue(is_perfect(maze))

    def test_42_pattern(self):
        """The 42 pattern is present and fully closed."""
        for width, height in [
            (9, 7),
            (10, 10),
            (15, 12),
        ]:
            with self.subTest(size=(width, height)):
                maze = MazeGenerator(
                    width, height, seed=42
                ).generate(perfect=True)

                self.assertEqual(len(maze.blocked), 18)

                for x, y in maze.blocked:
                    self.assertEqual(
                        maze.walls[y][x], 15
                    )

                self.assertTrue(validate_walls(maze))
                self.assertTrue(is_connected(maze))
                pattern = (
                    "#...###",
                    "#.....#",
                    "###.###",
                    "..#.#..",
                    "..#.###",
                )

                start_x = (width - 7) // 2
                start_y = (height - 5) // 2

                expected = {
                    (start_x + dx, start_y + dy)
                    for dy, row in enumerate(pattern)
                    for dx, char in enumerate(row)
                    if char == "#"
                }

                self.assertEqual(maze.blocked, expected)

    def test_same_seed(self):
        """Same inputs and seed give identical mazes."""
        for algorithm in ALGORITHMS:
            for perfect in (True, False):
                with self.subTest(
                    algorithm=algorithm,
                    perfect=perfect,
                ):
                    maze1 = MazeGenerator(
                        15, 12, seed=123
                    ).generate(
                        algorithm=algorithm,
                        perfect=perfect,
                    )

                    maze2 = MazeGenerator(
                        15, 12, seed=123
                    ).generate(
                        algorithm=algorithm,
                        perfect=perfect,
                    )

                    self.assertEqual(
                        maze1.walls, maze2.walls
                    )
                    self.assertEqual(
                        maze1.blocked, maze2.blocked
                    )

    def test_custom_entry_exit(self):
        """Custom entry and exit are stored correctly."""
        maze = MazeGenerator(
            15, 12, seed=42
        ).generate(
            algorithm="dfs",
            perfect=False,
            entry=(0, 5),
            exit=(14, 6),
        )

        self.assertEqual(maze.entry_point, (0, 5))
        self.assertEqual(maze.exit_point, (14, 6))
        self.assertTrue(is_connected(maze))

    def test_invalid_entry_exit(self):
        """Invalid entry and exit coordinates are rejected."""
        generator = MazeGenerator(15, 12, seed=42)

        invalid_cases = [
            ((0, 0), (0, 0)),     # Same coordinates
            ((-1, 0), (14, 11)),  # Negative x
            ((0, -1), (14, 11)),  # Negative y
            ((15, 0), (14, 11)),  # x too large
            ((0, 12), (14, 11)),  # y too large
            ((0, 0), (15, 11)),   # Exit outside
        ]

        for entry, exit_point in invalid_cases:
            with self.subTest(
                entry=entry,
                exit=exit_point,
            ):
                with self.assertRaises(ValueError):
                    generator.generate(
                        entry=entry,
                        exit=exit_point,
                    )

    def test_entry_inside_42(self):
        """Entry and exit cannot be blocked cells."""
        generator = MazeGenerator(15, 12, seed=42)

        blocked = generator._create_42_pattern()
        blocked_cell = next(iter(blocked))

        with self.assertRaises(ValueError):
            generator.generate(
                entry=blocked_cell,
                exit=(14, 11),
            )

        with self.assertRaises(ValueError):
            generator.generate(
                entry=(0, 0),
                exit=blocked_cell,
            )

    def test_invalid_dimensions(self):
        """Zero and negative dimensions are rejected."""
        for width, height in [
            (0, 5),
            (5, 0),
            (-1, 5),
            (5, -1),
        ]:
            with self.subTest(size=(width, height)):
                with self.assertRaises(ValueError):
                    MazeGenerator(width, height, 42)

    def test_impossible_non_perfect(self):
        """2x2 cannot contain 2 independent cycles."""
        with self.assertRaises(ValueError):
            MazeGenerator(
                2, 2, seed=42
            ).generate(perfect=False)

    def test_unknown_algorithm(self):
        """Unsupported algorithm names are rejected."""
        with self.assertRaises(ValueError):
            MazeGenerator(
                10, 10, 42
            ).generate(algorithm="invalid")

    def test_invalid_shared_wall(self):
        """Inconsistent neighbouring walls are rejected."""
        maze = Maze(
            width=2,
            height=2,
            walls=[[15, 15], [15, 15]],
            blocked=set(),
            entry_point=(0, 0),
            exit_point=(1, 1),
        )

        maze.walls[0][0] &= ~EAST

        self.assertFalse(validate_walls(maze))

    def test_invalid_boundary(self):
        """An open external wall is rejected."""
        maze = Maze(
            width=2,
            height=2,
            walls=[[15, 15], [15, 15]],
            blocked=set(),
            entry_point=(0, 0),
            exit_point=(1, 1),
        )

        maze.walls[0][0] &= ~NORTH

        self.assertFalse(validate_walls(maze))

    def test_open_3x3_detection(self):
        """A completely open 3x3 area is detected."""
        maze = Maze(
            width=3,
            height=3,
            walls=[[15] * 3 for _ in range(3)],
            blocked=set(),
            entry_point=(0, 0),
            exit_point=(2, 2),
        )

        # Open all 12 internal passages
        for y in range(3):
            for x in range(3):
                if x < 2:
                    maze.open_between(
                        (x, y), (x + 1, y)
                    )

                if y < 2:
                    maze.open_between(
                        (x, y), (x, y + 1)
                    )

        self.assertTrue(has_open_3x3(maze))

    def test_single_cell_maze(self):
        with self.assertRaises(ValueError):
            MazeGenerator(
                1, 1, seed=42
            ).generate(perfect=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
