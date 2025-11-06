"""
Constraint builders for common Zebra puzzle clue types.

These functions create constraint functions that can be added to a ZebraPuzzle.
"""

from typing import Dict, Optional, Callable


def same_position(category1: str, value1: str, category2: str, value2: str) -> Callable:
    """
    Create constraint: value1 in category1 is at the same position as value2 in category2.

    Example: "The Englishman lives in the red house"
    same_position('nationality', 'English', 'color', 'red')
    """
    def constraint(assignment: Dict[str, Dict[int, str]]) -> bool:
        pos1 = None
        pos2 = None

        # Find position of value1
        if category1 in assignment:
            for pos, val in assignment[category1].items():
                if val == value1:
                    pos1 = pos
                    break

        # Find position of value2
        if category2 in assignment:
            for pos, val in assignment[category2].items():
                if val == value2:
                    pos2 = pos
                    break

        # If both are assigned, they must be at same position
        if pos1 is not None and pos2 is not None:
            return pos1 == pos2

        # If only one is assigned, the other can still be placed there
        return True

    return constraint


def adjacent(category1: str, value1: str, category2: str, value2: str) -> Callable:
    """
    Create constraint: value1 and value2 are at adjacent positions.

    Example: "The person who owns the snail lives next to the person who drinks tea"
    adjacent('pet', 'snail', 'drink', 'tea')
    """
    def constraint(assignment: Dict[str, Dict[int, str]]) -> bool:
        pos1 = None
        pos2 = None

        # Find position of value1
        if category1 in assignment:
            for pos, val in assignment[category1].items():
                if val == value1:
                    pos1 = pos
                    break

        # Find position of value2
        if category2 in assignment:
            for pos, val in assignment[category2].items():
                if val == value2:
                    pos2 = pos
                    break

        # If both are assigned, they must be adjacent
        if pos1 is not None and pos2 is not None:
            return abs(pos1 - pos2) == 1

        return True

    return constraint


def left_of(category1: str, value1: str, category2: str, value2: str) -> Callable:
    """
    Create constraint: value1 is somewhere to the left of value2.

    Example: "The red house is to the left of the green house"
    left_of('color', 'red', 'color', 'green')
    """
    def constraint(assignment: Dict[str, Dict[int, str]]) -> bool:
        pos1 = None
        pos2 = None

        # Find position of value1
        if category1 in assignment:
            for pos, val in assignment[category1].items():
                if val == value1:
                    pos1 = pos
                    break

        # Find position of value2
        if category2 in assignment:
            for pos, val in assignment[category2].items():
                if val == value2:
                    pos2 = pos
                    break

        # If both are assigned, value1 must be to the left
        if pos1 is not None and pos2 is not None:
            return pos1 < pos2

        return True

    return constraint


def immediately_right_of(category1: str, value1: str, category2: str, value2: str) -> Callable:
    """
    Create constraint: value1 is immediately to the right of value2.

    Example: "The green house is immediately to the right of the red house"
    immediately_right_of('color', 'green', 'color', 'red')
    """
    def constraint(assignment: Dict[str, Dict[int, str]]) -> bool:
        pos1 = None
        pos2 = None

        # Find position of value1
        if category1 in assignment:
            for pos, val in assignment[category1].items():
                if val == value1:
                    pos1 = pos
                    break

        # Find position of value2
        if category2 in assignment:
            for pos, val in assignment[category2].items():
                if val == value2:
                    pos2 = pos
                    break

        # If both are assigned, value1 must be exactly one position to the right
        if pos1 is not None and pos2 is not None:
            return pos1 == pos2 + 1

        return True

    return constraint


def at_position(category: str, value: str, position: int) -> Callable:
    """
    Create constraint: value is at a specific position.

    Example: "The Norwegian lives in the first house"
    at_position('nationality', 'Norwegian', 0)
    """
    def constraint(assignment: Dict[str, Dict[int, str]]) -> bool:
        if category not in assignment:
            return True

        # Check if value is assigned
        for pos, val in assignment[category].items():
            if val == value:
                return pos == position

        # Check if position is assigned to something else
        if position in assignment[category]:
            return assignment[category][position] != value or assignment[category][position] == value

        return True

    return constraint


def at_edge(category: str, value: str, edge: str = 'either') -> Callable:
    """
    Create constraint: value is at the first or last position.

    Args:
        category: Category name
        value: Value to constrain
        edge: 'first', 'last', or 'either'

    Example: "The yellow house is at one end"
    at_edge('color', 'yellow', 'either')
    """
    def constraint(assignment: Dict[str, Dict[int, str]]) -> bool:
        if category not in assignment:
            return True

        # Find position of value
        pos = None
        for p, val in assignment[category].items():
            if val == value:
                pos = p
                break

        if pos is None:
            return True

        # Determine number of positions from assignment
        num_positions = max(assignment[category].keys()) + 1

        if edge == 'first':
            return pos == 0
        elif edge == 'last':
            return pos == num_positions - 1
        elif edge == 'either':
            return pos == 0 or pos == num_positions - 1
        else:
            raise ValueError(f"Invalid edge value: {edge}")

    return constraint


def middle_position(category: str, value: str, num_positions: int) -> Callable:
    """
    Create constraint: value is in the middle position (only for odd number of positions).

    Example: "The milk is drunk in the middle house" (for 5 houses)
    middle_position('drink', 'milk', 5)
    """
    if num_positions % 2 == 0:
        raise ValueError("middle_position only works with odd number of positions")

    middle = num_positions // 2

    def constraint(assignment: Dict[str, Dict[int, str]]) -> bool:
        if category not in assignment:
            return True

        # Find position of value
        for pos, val in assignment[category].items():
            if val == value:
                return pos == middle

        return True

    return constraint


def one_of_positions(category: str, value: str, positions: list) -> Callable:
    """
    Create constraint: value is at one of the specified positions.

    Example: "The fox is in house 1, 2, or 3"
    one_of_positions('pet', 'fox', [0, 1, 2])
    """
    def constraint(assignment: Dict[str, Dict[int, str]]) -> bool:
        if category not in assignment:
            return True

        # Find position of value
        for pos, val in assignment[category].items():
            if val == value:
                return pos in positions

        return True

    return constraint


def not_same_position(category1: str, value1: str, category2: str, value2: str) -> Callable:
    """
    Create constraint: value1 and value2 are NOT at the same position.

    Example: "The person who drinks water doesn't live in the red house"
    not_same_position('drink', 'water', 'color', 'red')
    """
    def constraint(assignment: Dict[str, Dict[int, str]]) -> bool:
        pos1 = None
        pos2 = None

        # Find position of value1
        if category1 in assignment:
            for pos, val in assignment[category1].items():
                if val == value1:
                    pos1 = pos
                    break

        # Find position of value2
        if category2 in assignment:
            for pos, val in assignment[category2].items():
                if val == value2:
                    pos2 = pos
                    break

        # If both are assigned, they must NOT be at same position
        if pos1 is not None and pos2 is not None:
            return pos1 != pos2

        return True

    return constraint
