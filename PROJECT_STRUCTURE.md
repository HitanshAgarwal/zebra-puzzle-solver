# Zebra Puzzle Solver - Project Structure

## Overview
A complete Einstein-style logic puzzle solver with both command-line and web interfaces.

## File Structure

```
einstein-puzzles/
├── Core Solver
│   ├── zebra_solver.py          # Main CSP solver engine
│   └── constraints.py            # Constraint type definitions
│
├── Example Puzzles
│   ├── example_puzzle.py         # 3-house example puzzle
│   └── einstein_puzzle.py        # Classic 5-house Einstein puzzle
│
├── Web Application
│   ├── web_app.py                # Flask backend server
│   ├── templates/
│   │   └── index.html            # Main web interface
│   └── static/
│       ├── css/
│       │   └── style.css         # Styling and layout
│       └── js/
│           └── app.js            # Frontend logic
│
├── Documentation
│   ├── README.md                 # Main documentation
│   ├── USAGE.md                  # Detailed usage guide
│   └── PROJECT_STRUCTURE.md      # This file
│
├── Configuration
│   ├── requirements.txt          # Python dependencies
│   ├── start.sh                  # Startup script
│   └── .gitignore                # Git ignore rules
│
└── .claude/                      # Claude Code configuration
```

## Core Components

### Solver Engine (`zebra_solver.py`)
- **ZebraPuzzle class**: Main puzzle representation
- **Backtracking search**: With constraint propagation
- **Domain reduction**: MRV heuristic for variable selection
- **Constraint checking**: Validates partial assignments

### Constraints (`constraints.py`)
Factory functions for creating constraint predicates:
- `same_position()` - Two values at same position
- `adjacent()` - Values next to each other
- `immediately_right_of()` - Exactly one position to the right
- `left_of()` - Somewhere to the left
- `at_position()` - At specific position (0-indexed)
- `middle_position()` - In the center
- `not_same_position()` - Not at same position

### Web Application (`web_app.py`)
Flask server with endpoints:
- `GET /` - Main web interface
- `POST /solve` - Solve puzzle endpoint
- `GET /presets` - Get preset puzzles

### Frontend (`templates/index.html`, `static/`)
- Dynamic form for puzzle configuration
- Preset puzzle loading
- Real-time constraint editing
- Solution display in table format
- Responsive design with gradient theme

## Command-Line Usage

```bash
# Run preset puzzles
python3 example_puzzle.py
python3 einstein_puzzle.py

# Start web server
python3 web_app.py
# or
./start.sh
```

## Web Interface Usage

1. Start server: `python3 web_app.py`
2. Open browser: `http://127.0.0.1:5001`
3. Load preset or create custom puzzle
4. Click "Solve Puzzle"

## Dependencies

- **Python 3.7+**
- **Flask 3.0+** (for web interface)

Install with:
```bash
pip install -r requirements.txt
```

## Key Features

- ✅ Constraint Satisfaction Problem (CSP) solver
- ✅ 7 different constraint types
- ✅ Web interface with dynamic forms
- ✅ Preset puzzles (3-house and 5-house)
- ✅ Custom puzzle creation
- ✅ Real-time validation
- ✅ Responsive design
- ✅ Command-line examples

## Algorithm

The solver uses:
1. **Domain initialization** - All values possible for each position
2. **Constraint propagation** - Reduce domains using constraints
3. **Backtracking search** - Try assignments and backtrack on failure
4. **MRV heuristic** - Select variable with minimum remaining values
5. **Forward checking** - Update domains after each assignment

## Performance

- 3-house puzzles: < 0.1 seconds
- 5-house Einstein puzzle: 1-2 seconds
- Handles up to 7 positions efficiently

## Code Quality

- Type hints for better IDE support
- Comprehensive docstrings
- Modular design
- Separation of concerns (solver, constraints, UI)
- Clean codebase with no test artifacts

## Future Enhancements

Possible improvements:
- Arc consistency (AC-3 algorithm)
- More constraint types
- Puzzle difficulty rating
- Solution uniqueness verification
- Export puzzles to JSON
- Puzzle library/database
