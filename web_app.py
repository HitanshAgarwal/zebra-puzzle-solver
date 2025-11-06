"""
Flask web application for the Zebra Puzzle Solver.

Provides a web interface for users to configure and solve puzzles.
"""

from flask import Flask, render_template, request, jsonify
from zebra_solver import ZebraPuzzle
from constraints import (
    same_position, adjacent, immediately_right_of, at_position,
    middle_position, left_of, not_same_position
)
import json

app = Flask(__name__)


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve_puzzle():
    """
    Solve a puzzle based on the provided configuration.

    Expected JSON format:
    {
        "num_positions": 5,
        "categories": {
            "nationality": ["Brit", "Swede", ...],
            "color": ["red", "green", ...]
        },
        "constraints": [
            {
                "type": "same_position",
                "params": ["nationality", "Brit", "color", "red"],
                "description": "The Brit lives in the red house"
            },
            ...
        ]
    }
    """
    try:
        data = request.json
        num_positions = data['num_positions']
        categories = data['categories']
        constraints_data = data['constraints']

        # Create puzzle
        puzzle = ZebraPuzzle(num_positions, categories)

        # Add constraints
        constraint_map = {
            'same_position': same_position,
            'adjacent': adjacent,
            'immediately_right_of': immediately_right_of,
            'at_position': at_position,
            'middle_position': middle_position,
            'left_of': left_of,
            'not_same_position': not_same_position
        }

        for constraint_data in constraints_data:
            constraint_type = constraint_data['type']
            params = constraint_data['params']
            description = constraint_data.get('description', '')

            if constraint_type in constraint_map:
                constraint_func = constraint_map[constraint_type](*params)
                puzzle.add_constraint(constraint_func, description)

        # Solve puzzle
        solution = puzzle.solve()

        if solution is None:
            return jsonify({
                'success': False,
                'error': 'No solution found. The constraints may be inconsistent.'
            })

        # Format solution for display
        formatted_solution = []
        for pos in range(num_positions):
            position_data = {'position': pos + 1}
            for category, assignments in solution.items():
                position_data[category] = assignments[pos]
            formatted_solution.append(position_data)

        return jsonify({
            'success': True,
            'solution': formatted_solution,
            'categories': list(categories.keys())
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/presets')
def get_presets():
    """Get preset puzzles."""
    presets = {
        'example': {
            'name': '3-House Example',
            'num_positions': 3,
            'categories': {
                'nationality': ['English', 'Spanish', 'Japanese'],
                'color': ['red', 'green', 'ivory'],
                'pet': ['dog', 'snail', 'fox'],
                'drink': ['coffee', 'tea', 'water']
            },
            'constraints': [
                {
                    'type': 'same_position',
                    'params': ['nationality', 'English', 'color', 'red'],
                    'description': 'The Englishman lives in the red house'
                },
                {
                    'type': 'same_position',
                    'params': ['nationality', 'Spanish', 'pet', 'dog'],
                    'description': 'The Spaniard owns the dog'
                },
                {
                    'type': 'same_position',
                    'params': ['drink', 'coffee', 'color', 'green'],
                    'description': 'Coffee is drunk in the green house'
                },
                {
                    'type': 'immediately_right_of',
                    'params': ['color', 'green', 'color', 'red'],
                    'description': 'The green house is immediately to the right of the red house'
                },
                {
                    'type': 'adjacent',
                    'params': ['pet', 'snail', 'drink', 'tea'],
                    'description': 'The person who owns the snail lives next to the person who drinks tea'
                },
                {
                    'type': 'adjacent',
                    'params': ['nationality', 'Japanese', 'pet', 'snail'],
                    'description': 'The Japanese lives next to the snail owner'
                }
            ]
        },
        'einstein': {
            'name': 'Classic Einstein Puzzle (5 Houses)',
            'num_positions': 5,
            'categories': {
                'nationality': ['Brit', 'Swede', 'Dane', 'Norwegian', 'German'],
                'color': ['red', 'green', 'white', 'yellow', 'blue'],
                'drink': ['tea', 'coffee', 'milk', 'beer', 'water'],
                'cigar': ['Pall Mall', 'Dunhill', 'Blends', 'BlueMaster', 'Prince'],
                'pet': ['dogs', 'birds', 'cats', 'horse', 'fish']
            },
            'constraints': [
                {
                    'type': 'same_position',
                    'params': ['nationality', 'Brit', 'color', 'red'],
                    'description': 'The Brit lives in the red house'
                },
                {
                    'type': 'same_position',
                    'params': ['nationality', 'Swede', 'pet', 'dogs'],
                    'description': 'The Swede keeps dogs as pets'
                },
                {
                    'type': 'same_position',
                    'params': ['nationality', 'Dane', 'drink', 'tea'],
                    'description': 'The Dane drinks tea'
                },
                {
                    'type': 'immediately_right_of',
                    'params': ['color', 'white', 'color', 'green'],
                    'description': 'The green house is immediately to the left of the white house'
                },
                {
                    'type': 'same_position',
                    'params': ['color', 'green', 'drink', 'coffee'],
                    'description': "The green house's owner drinks coffee"
                },
                {
                    'type': 'same_position',
                    'params': ['cigar', 'Pall Mall', 'pet', 'birds'],
                    'description': 'The person who smokes Pall Mall rears birds'
                },
                {
                    'type': 'same_position',
                    'params': ['color', 'yellow', 'cigar', 'Dunhill'],
                    'description': 'The owner of the yellow house smokes Dunhill'
                },
                {
                    'type': 'middle_position',
                    'params': ['drink', 'milk', 5],
                    'description': 'The man living in the center house drinks milk'
                },
                {
                    'type': 'at_position',
                    'params': ['nationality', 'Norwegian', 0],
                    'description': 'The Norwegian lives in the first house'
                },
                {
                    'type': 'adjacent',
                    'params': ['cigar', 'Blends', 'pet', 'cats'],
                    'description': 'The man who smokes Blends lives next to the one who keeps cats'
                },
                {
                    'type': 'adjacent',
                    'params': ['pet', 'horse', 'cigar', 'Dunhill'],
                    'description': 'The man who keeps a horse lives next to the man who smokes Dunhill'
                },
                {
                    'type': 'same_position',
                    'params': ['cigar', 'BlueMaster', 'drink', 'beer'],
                    'description': 'The owner who smokes BlueMaster drinks beer'
                },
                {
                    'type': 'same_position',
                    'params': ['nationality', 'German', 'cigar', 'Prince'],
                    'description': 'The German smokes Prince'
                },
                {
                    'type': 'adjacent',
                    'params': ['nationality', 'Norwegian', 'color', 'blue'],
                    'description': 'The Norwegian lives next to the blue house'
                },
                {
                    'type': 'adjacent',
                    'params': ['cigar', 'Blends', 'drink', 'water'],
                    'description': 'The man who smokes Blends has a neighbor who drinks water'
                }
            ]
        }
    }
    return jsonify(presets)


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    print(f"\n{'='*70}")
    print(f"🧩 Zebra Puzzle Solver Web Interface")
    print(f"{'='*70}")
    print(f"Server starting on http://127.0.0.1:{port}")
    print(f"Open this URL in your browser to use the puzzle solver.")
    print(f"{'='*70}\n")
    app.run(debug=True, port=port)
