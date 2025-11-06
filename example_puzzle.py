"""
Example 3-house puzzle from the problem description.

Puzzle:
There are three houses in a row.
 - The Englishman lives in the red house.
 - The Spaniard owns the dog.
 - Coffee is drunk in the green house.
 - The green house is immediately to the right of the red house.
 - The person who owns the snail lives next to the person who drinks tea.
 - The Japanese lives next to the snail owner.

Questions:
 - Who drinks coffee?
 - Who owns the dog?
"""

from zebra_solver import ZebraPuzzle, print_solution, query_solution
from constraints import same_position, adjacent, immediately_right_of


def create_example_puzzle():
    """Create and return the 3-house example puzzle."""

    # Define categories and their values
    categories = {
        'nationality': ['English', 'Spanish', 'Japanese'],
        'color': ['red', 'green', 'ivory'],  # Added ivory for the third house
        'pet': ['dog', 'snail', 'fox'],      # Added fox for the third pet
        'drink': ['coffee', 'tea', 'water']  # Added water for the third drink
    }

    # Create puzzle
    puzzle = ZebraPuzzle(num_positions=3, categories=categories)

    # Add constraints based on clues

    # The Englishman lives in the red house
    puzzle.add_constraint(
        same_position('nationality', 'English', 'color', 'red'),
        "The Englishman lives in the red house"
    )

    # The Spaniard owns the dog
    puzzle.add_constraint(
        same_position('nationality', 'Spanish', 'pet', 'dog'),
        "The Spaniard owns the dog"
    )

    # Coffee is drunk in the green house
    puzzle.add_constraint(
        same_position('drink', 'coffee', 'color', 'green'),
        "Coffee is drunk in the green house"
    )

    # The green house is immediately to the right of the red house
    puzzle.add_constraint(
        immediately_right_of('color', 'green', 'color', 'red'),
        "The green house is immediately to the right of the red house"
    )

    # The person who owns the snail lives next to the person who drinks tea
    puzzle.add_constraint(
        adjacent('pet', 'snail', 'drink', 'tea'),
        "The person who owns the snail lives next to the person who drinks tea"
    )

    # The Japanese lives next to the snail owner
    puzzle.add_constraint(
        adjacent('nationality', 'Japanese', 'pet', 'snail'),
        "The Japanese lives next to the snail owner"
    )

    return puzzle


def solve_example():
    """Solve the example puzzle and answer the questions."""
    print("=" * 70)
    print("EXAMPLE PUZZLE: 3 Houses")
    print("=" * 70)
    print("\nClues:")
    print("1. The Englishman lives in the red house")
    print("2. The Spaniard owns the dog")
    print("3. Coffee is drunk in the green house")
    print("4. The green house is immediately to the right of the red house")
    print("5. The person who owns the snail lives next to the person who drinks tea")
    print("6. The Japanese lives next to the snail owner")
    print()

    puzzle = create_example_puzzle()
    solution = puzzle.solve()

    print_solution(solution, puzzle.num_positions)

    if solution:
        print("\nAnswers to questions:")
        print("-" * 70)

        # Who drinks coffee?
        coffee_info = query_solution(solution, 'drink', 'coffee')
        if coffee_info:
            print(f"Who drinks coffee? The {coffee_info['nationality']}")

        # Who owns the dog?
        dog_info = query_solution(solution, 'pet', 'dog')
        if dog_info:
            print(f"Who owns the dog? The {dog_info['nationality']}")

        print()

    return solution


if __name__ == "__main__":
    solve_example()
