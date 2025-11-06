# Zebra Puzzle Solver

A constraint satisfaction problem (CSP) solver for Einstein-style logic puzzles, with a web interface for easy puzzle configuration and solving.

## Features

- **Powerful CSP Solver**: Uses backtracking with constraint propagation to efficiently solve logic puzzles
- **Web Interface**: User-friendly HTML/CSS/JS frontend for configuring puzzles
- **Preset Puzzles**: Includes the classic 5-house Einstein puzzle and a 3-house example
- **Custom Puzzles**: Create your own puzzles with custom categories and constraints
- **Multiple Constraint Types**:
  - Same position
  - Adjacent
  - Immediately right/left of
  - At specific position
  - Middle position
  - Not same position

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface

1. Start the Flask server:
```bash
python3 web_app.py
```

Or specify a custom port (macOS users: port 5000 may be used by AirPlay):
```bash
python3 web_app.py 8080
```

2. Open your browser and navigate to:
```
http://localhost:5001
```

Or your custom port:
```
http://localhost:8080
```

3. Choose a preset puzzle or create your own custom puzzle by:
   - Setting the number of positions (houses)
   - Defining categories and their values
   - Adding constraints (clues)
   - Clicking "Solve Puzzle"

### Command Line

Run the example puzzles directly:

```bash
# 3-house example puzzle
python3 example_puzzle.py

# Classic Einstein puzzle (5 houses)
python3 einstein_puzzle.py
```

### Programmatic Usage

```python
from zebra_solver import ZebraPuzzle
from constraints import same_position, adjacent

# Define categories
categories = {
    'nationality': ['English', 'Spanish', 'Japanese'],
    'color': ['red', 'green', 'ivory'],
    'pet': ['dog', 'snail', 'fox'],
    'drink': ['coffee', 'tea', 'water']
}

# Create puzzle
puzzle = ZebraPuzzle(num_positions=3, categories=categories)

# Add constraints
puzzle.add_constraint(
    same_position('nationality', 'English', 'color', 'red'),
    "The Englishman lives in the red house"
)

puzzle.add_constraint(
    adjacent('pet', 'snail', 'drink', 'tea'),
    "The snail owner lives next to the tea drinker"
)

# Solve
solution = puzzle.solve()
```

## Architecture

### Core Components

1. **zebra_solver.py**: Main CSP solver implementation
   - `ZebraPuzzle`: Puzzle representation and solver
   - Backtracking search with MRV heuristic
   - Domain reduction and constraint propagation

2. **constraints.py**: Constraint builders for common clue types
   - Factory functions for creating constraint predicates
   - Supports various spatial and logical relationships

3. **web_app.py**: Flask backend
   - REST API for solving puzzles
   - Preset puzzle management
   - JSON-based puzzle configuration

4. **Frontend** (templates/ and static/):
   - Responsive HTML/CSS interface
   - Dynamic constraint configuration
   - Real-time solution display

## Constraint Types

### Same Position
Two values are at the same position.
```python
same_position('nationality', 'Brit', 'color', 'red')
# The Brit lives in the red house
```

### Adjacent
Two values are at adjacent positions.
```python
adjacent('pet', 'snail', 'drink', 'tea')
# The snail owner lives next to the tea drinker
```

### Immediately Right Of
One value is exactly one position to the right of another.
```python
immediately_right_of('color', 'green', 'color', 'red')
# The green house is immediately to the right of the red house
```

### Left Of
One value is somewhere to the left of another.
```python
left_of('color', 'red', 'color', 'green')
# The red house is to the left of the green house
```

### At Position
A value is at a specific position (0-indexed).
```python
at_position('nationality', 'Norwegian', 0)
# The Norwegian lives in the first house
```

### Middle Position
A value is in the middle position (odd number of positions only).
```python
middle_position('drink', 'milk', 5)
# Milk is drunk in the middle house
```

### Not Same Position
Two values are NOT at the same position.
```python
not_same_position('drink', 'water', 'color', 'red')
# The person who drinks water doesn't live in the red house
```

## Example Puzzles

### 3-House Example
A simple puzzle with 4 categories and 6 constraints.

**Categories**: nationality, color, pet, drink

**Question**: Who drinks coffee? Who owns the dog?

**Answer**: The Spanish drinks coffee and owns the dog.

### Classic Einstein Puzzle
The famous 5-house puzzle with 5 categories and 15 constraints.

**Categories**: nationality, color, drink, cigar, pet

**Question**: Who owns the fish?

**Answer**: The German owns the fish.

## Algorithm

The solver uses a **Constraint Satisfaction Problem (CSP)** approach:

1. **Domain Initialization**: Each position can have any value from each category
2. **Constraint Propagation**: Reduce domains by applying constraints
3. **Backtracking Search**:
   - Select unassigned variable using MRV (Minimum Remaining Values) heuristic
   - Try each value in the domain
   - Check consistency with constraints
   - Recursively solve or backtrack

## Performance

The solver efficiently handles puzzles with:
- 3-7 positions
- 3-6 categories
- 10-20 constraints

The classic Einstein puzzle (5 positions, 5 categories, 15 constraints) solves in under a second.

## License

MIT License - feel free to use and modify as needed.
