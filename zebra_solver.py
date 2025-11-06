"""
Zebra Puzzle Solver using Constraint Satisfaction Problem (CSP) approach.

This solver uses backtracking with constraint propagation to solve
Einstein-style logic puzzles.
"""

from typing import Dict, List, Set, Tuple, Optional, Callable
from itertools import permutations
from copy import deepcopy


class ZebraPuzzle:
    """
    Represents a Zebra puzzle with positions, categories, and constraints.

    Example structure:
    - num_positions: 5 (e.g., 5 houses)
    - categories: {'nationality': ['English', 'Spanish', ...],
                   'color': ['red', 'green', ...], ...}
    - constraints: List of constraint functions
    """

    def __init__(self, num_positions: int, categories: Dict[str, List[str]]):
        """
        Initialize a Zebra puzzle.

        Args:
            num_positions: Number of positions (e.g., houses)
            categories: Dictionary mapping category names to possible values
        """
        self.num_positions = num_positions
        self.categories = categories
        self.constraints = []

        # Validate that all categories have the correct number of values
        for category, values in categories.items():
            if len(values) != num_positions:
                raise ValueError(
                    f"Category '{category}' has {len(values)} values, "
                    f"expected {num_positions}"
                )

    def add_constraint(self, constraint_func: Callable, description: str = ""):
        """
        Add a constraint to the puzzle.

        Args:
            constraint_func: Function that takes an assignment dict and returns bool
            description: Human-readable description of the constraint
        """
        self.constraints.append({
            'func': constraint_func,
            'description': description
        })

    def solve(self) -> Optional[Dict[str, Dict[int, str]]]:
        """
        Solve the puzzle using backtracking with constraint propagation.

        Returns:
            Dictionary mapping categories to position->value assignments,
            or None if no solution exists.
        """
        # Initialize domains: for each category and position, track possible values
        domains = {}
        for category, values in self.categories.items():
            domains[category] = {pos: set(values) for pos in range(self.num_positions)}

        # Apply initial constraint propagation
        domains = self._propagate_constraints(domains)
        if domains is None:
            return None

        # Start backtracking search
        return self._backtrack({}, domains)

    def _backtrack(
        self,
        assignment: Dict[str, Dict[int, str]],
        domains: Dict[str, Dict[int, Set[str]]]
    ) -> Optional[Dict[str, Dict[int, str]]]:
        """
        Recursive backtracking search.

        Args:
            assignment: Current partial assignment
            domains: Current domains for each category/position

        Returns:
            Complete assignment if solution found, None otherwise
        """
        # Check if assignment is complete
        if self._is_complete(assignment):
            return assignment

        # Select unassigned variable (category, position)
        category, position = self._select_unassigned_variable(assignment, domains)

        # Try each value in the domain
        for value in list(domains[category][position]):
            # Make assignment
            new_assignment = deepcopy(assignment)
            if category not in new_assignment:
                new_assignment[category] = {}
            new_assignment[category][position] = value

            # Check if assignment is consistent
            if self._is_consistent(new_assignment):
                # Propagate constraints
                new_domains = self._update_domains(domains, category, position, value)
                new_domains = self._propagate_constraints(new_domains, new_assignment)

                if new_domains is not None:
                    # Recurse
                    result = self._backtrack(new_assignment, new_domains)
                    if result is not None:
                        return result

        return None

    def _is_complete(self, assignment: Dict[str, Dict[int, str]]) -> bool:
        """Check if assignment is complete."""
        for category in self.categories:
            if category not in assignment:
                return False
            if len(assignment[category]) != self.num_positions:
                return False
        return True

    def _select_unassigned_variable(
        self,
        assignment: Dict[str, Dict[int, str]],
        domains: Dict[str, Dict[int, Set[str]]]
    ) -> Tuple[str, int]:
        """
        Select next variable to assign using MRV (Minimum Remaining Values) heuristic.

        Returns:
            Tuple of (category, position)
        """
        min_remaining = float('inf')
        best_var = None

        for category in self.categories:
            for position in range(self.num_positions):
                # Skip if already assigned
                if category in assignment and position in assignment[category]:
                    continue

                remaining = len(domains[category][position])
                if remaining < min_remaining:
                    min_remaining = remaining
                    best_var = (category, position)

        return best_var

    def _is_consistent(self, assignment: Dict[str, Dict[int, str]]) -> bool:
        """Check if current assignment satisfies all constraints."""
        for constraint in self.constraints:
            if not constraint['func'](assignment):
                return False
        return True

    def _update_domains(
        self,
        domains: Dict[str, Dict[int, Set[str]]],
        category: str,
        position: int,
        value: str
    ) -> Dict[str, Dict[int, Set[str]]]:
        """
        Update domains after making an assignment.
        Removes the assigned value from other positions in the same category,
        and removes the assigned position from other values.
        """
        new_domains = deepcopy(domains)

        # Set the assigned value
        new_domains[category][position] = {value}

        # Remove value from other positions in same category
        for pos in range(self.num_positions):
            if pos != position:
                new_domains[category][pos].discard(value)

        return new_domains

    def _propagate_constraints(
        self,
        domains: Dict[str, Dict[int, Set[str]]],
        assignment: Optional[Dict[str, Dict[int, str]]] = None
    ) -> Optional[Dict[str, Dict[int, Set[str]]]]:
        """
        Propagate constraints to reduce domains.

        Returns:
            Updated domains, or None if inconsistency detected
        """
        if assignment is None:
            assignment = {}

        changed = True
        while changed:
            changed = False

            # Check for domain wipeout
            for category in domains:
                for position in domains[category]:
                    if len(domains[category][position]) == 0:
                        return None

            # If a position has only one possible value, assign it
            for category in domains:
                for position in domains[category]:
                    if len(domains[category][position]) == 1:
                        value = list(domains[category][position])[0]

                        # Remove from other positions
                        for pos in range(self.num_positions):
                            if pos != position and value in domains[category][pos]:
                                domains[category][pos].remove(value)
                                changed = True

            # If a value can only go in one position, assign it there
            for category in domains:
                for value in self.categories[category]:
                    possible_positions = [
                        pos for pos in range(self.num_positions)
                        if value in domains[category][pos]
                    ]

                    if len(possible_positions) == 0:
                        return None
                    elif len(possible_positions) == 1:
                        pos = possible_positions[0]
                        if len(domains[category][pos]) > 1:
                            domains[category][pos] = {value}
                            changed = True

        return domains


def print_solution(solution: Dict[str, Dict[int, str]], num_positions: int):
    """Pretty print the solution."""
    if solution is None:
        print("No solution found!")
        return

    print("\nSolution found!")
    print("=" * 60)

    # Print header
    categories = list(solution.keys())
    header = f"{'Position':<12}"
    for category in categories:
        header += f"{category.capitalize():<15}"
    print(header)
    print("-" * 60)

    # Print each position
    for pos in range(num_positions):
        row = f"{pos + 1:<12}"
        for category in categories:
            row += f"{solution[category][pos]:<15}"
        print(row)

    print("=" * 60)


def query_solution(
    solution: Dict[str, Dict[int, str]],
    category: str,
    value: str
) -> Optional[Dict[str, str]]:
    """
    Query the solution to find what's at the position with a given value.

    Args:
        solution: The solved puzzle
        category: Category to search in
        value: Value to find

    Returns:
        Dictionary of all category values at that position
    """
    if solution is None or category not in solution:
        return None

    # Find position with the value
    position = None
    for pos, val in solution[category].items():
        if val == value:
            position = pos
            break

    if position is None:
        return None

    # Get all values at this position
    result = {}
    for cat, assignments in solution.items():
        result[cat] = assignments[position]

    return result
