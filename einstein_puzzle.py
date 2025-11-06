"""
The Classic Einstein Puzzle (5 houses).

This is the famous puzzle allegedly created by Einstein, who claimed only 2%
of the world could solve it.

The puzzle:
There are 5 houses in a row, each with a different color.
In each house lives a person of a different nationality.
Each person drinks a different beverage, smokes a different brand of cigar,
and keeps a different pet.

Clues:
1. The Brit lives in the red house.
2. The Swede keeps dogs as pets.
3. The Dane drinks tea.
4. The green house is on the left of the white house (next to it).
5. The green house's owner drinks coffee.
6. The person who smokes Pall Mall rears birds.
7. The owner of the yellow house smokes Dunhill.
8. The man living in the center house drinks milk.
9. The Norwegian lives in the first house.
10. The man who smokes Blends lives next to the one who keeps cats.
11. The man who keeps a horse lives next to the man who smokes Dunhill.
12. The owner who smokes BlueMaster drinks beer.
13. The German smokes Prince.
14. The Norwegian lives next to the blue house.
15. The man who smokes Blends has a neighbor who drinks water.

Question: Who owns the fish?
"""

from zebra_solver import ZebraPuzzle, print_solution, query_solution
from constraints import (
    same_position, adjacent, immediately_right_of, at_position, middle_position
)


def create_einstein_puzzle():
    """Create and return the classic 5-house Einstein puzzle."""

    # Define categories and their values
    categories = {
        'nationality': ['Brit', 'Swede', 'Dane', 'Norwegian', 'German'],
        'color': ['red', 'green', 'white', 'yellow', 'blue'],
        'drink': ['tea', 'coffee', 'milk', 'beer', 'water'],
        'cigar': ['Pall Mall', 'Dunhill', 'Blends', 'BlueMaster', 'Prince'],
        'pet': ['dogs', 'birds', 'cats', 'horse', 'fish']
    }

    # Create puzzle
    puzzle = ZebraPuzzle(num_positions=5, categories=categories)

    # Add constraints based on clues

    # 1. The Brit lives in the red house
    puzzle.add_constraint(
        same_position('nationality', 'Brit', 'color', 'red'),
        "The Brit lives in the red house"
    )

    # 2. The Swede keeps dogs as pets
    puzzle.add_constraint(
        same_position('nationality', 'Swede', 'pet', 'dogs'),
        "The Swede keeps dogs as pets"
    )

    # 3. The Dane drinks tea
    puzzle.add_constraint(
        same_position('nationality', 'Dane', 'drink', 'tea'),
        "The Dane drinks tea"
    )

    # 4. The green house is on the left of the white house (immediately to the left)
    puzzle.add_constraint(
        immediately_right_of('color', 'white', 'color', 'green'),
        "The green house is immediately to the left of the white house"
    )

    # 5. The green house's owner drinks coffee
    puzzle.add_constraint(
        same_position('color', 'green', 'drink', 'coffee'),
        "The green house's owner drinks coffee"
    )

    # 6. The person who smokes Pall Mall rears birds
    puzzle.add_constraint(
        same_position('cigar', 'Pall Mall', 'pet', 'birds'),
        "The person who smokes Pall Mall rears birds"
    )

    # 7. The owner of the yellow house smokes Dunhill
    puzzle.add_constraint(
        same_position('color', 'yellow', 'cigar', 'Dunhill'),
        "The owner of the yellow house smokes Dunhill"
    )

    # 8. The man living in the center house drinks milk
    puzzle.add_constraint(
        middle_position('drink', 'milk', 5),
        "The man living in the center house drinks milk"
    )

    # 9. The Norwegian lives in the first house
    puzzle.add_constraint(
        at_position('nationality', 'Norwegian', 0),
        "The Norwegian lives in the first house"
    )

    # 10. The man who smokes Blends lives next to the one who keeps cats
    puzzle.add_constraint(
        adjacent('cigar', 'Blends', 'pet', 'cats'),
        "The man who smokes Blends lives next to the one who keeps cats"
    )

    # 11. The man who keeps a horse lives next to the man who smokes Dunhill
    puzzle.add_constraint(
        adjacent('pet', 'horse', 'cigar', 'Dunhill'),
        "The man who keeps a horse lives next to the man who smokes Dunhill"
    )

    # 12. The owner who smokes BlueMaster drinks beer
    puzzle.add_constraint(
        same_position('cigar', 'BlueMaster', 'drink', 'beer'),
        "The owner who smokes BlueMaster drinks beer"
    )

    # 13. The German smokes Prince
    puzzle.add_constraint(
        same_position('nationality', 'German', 'cigar', 'Prince'),
        "The German smokes Prince"
    )

    # 14. The Norwegian lives next to the blue house
    puzzle.add_constraint(
        adjacent('nationality', 'Norwegian', 'color', 'blue'),
        "The Norwegian lives next to the blue house"
    )

    # 15. The man who smokes Blends has a neighbor who drinks water
    puzzle.add_constraint(
        adjacent('cigar', 'Blends', 'drink', 'water'),
        "The man who smokes Blends has a neighbor who drinks water"
    )

    return puzzle


def solve_einstein():
    """Solve the Einstein puzzle and answer the question."""
    print("=" * 70)
    print("THE CLASSIC EINSTEIN PUZZLE: 5 Houses")
    print("=" * 70)
    print("\nClues:")
    print(" 1. The Brit lives in the red house")
    print(" 2. The Swede keeps dogs as pets")
    print(" 3. The Dane drinks tea")
    print(" 4. The green house is on the left of the white house")
    print(" 5. The green house's owner drinks coffee")
    print(" 6. The person who smokes Pall Mall rears birds")
    print(" 7. The owner of the yellow house smokes Dunhill")
    print(" 8. The man living in the center house drinks milk")
    print(" 9. The Norwegian lives in the first house")
    print("10. The man who smokes Blends lives next to the one who keeps cats")
    print("11. The man who keeps a horse lives next to the man who smokes Dunhill")
    print("12. The owner who smokes BlueMaster drinks beer")
    print("13. The German smokes Prince")
    print("14. The Norwegian lives next to the blue house")
    print("15. The man who smokes Blends has a neighbor who drinks water")
    print()

    puzzle = create_einstein_puzzle()
    print("Solving... (this may take a moment)")
    solution = puzzle.solve()

    print_solution(solution, puzzle.num_positions)

    if solution:
        print("\nAnswer to the question:")
        print("-" * 70)

        # Who owns the fish?
        fish_info = query_solution(solution, 'pet', 'fish')
        if fish_info:
            print(f"Who owns the fish? The {fish_info['nationality']}")
            print()

    return solution


if __name__ == "__main__":
    solve_einstein()
