# Zebra Puzzle Solver - Usage Guide

## Quick Start

### 1. Start the Web Application

```bash
python3 web_app.py
```

The server will start on `http://localhost:5000`

### 2. Open in Browser

Navigate to `http://localhost:5000` in your web browser.

## Using the Web Interface

### Option 1: Load a Preset Puzzle

Click one of the preset buttons:
- **3-House Example**: A simple introductory puzzle
- **Classic Einstein (5 Houses)**: The famous Einstein puzzle

The form will automatically populate with:
- Categories and their values
- All constraints (clues)

Click **"Solve Puzzle"** to see the solution!

### Option 2: Create a Custom Puzzle

#### Step 1: Set Number of Positions
Enter the number of positions (e.g., 3 for 3 houses, 5 for 5 houses)

#### Step 2: Define Categories
For each category:
- Enter the category name (e.g., "color", "nationality")
- Enter comma-separated values (e.g., "red,green,blue")
- Number of values must match the number of positions
- Use **Add Category** to add more categories
- Use **Remove** to delete a category

Example:
```
Category: nationality
Values: Brit,Swede,Dane,Norwegian,German

Category: color
Values: red,green,white,yellow,blue
```

#### Step 3: Add Constraints
Click **Add Constraint** for each clue. Select the constraint type:

**Same Position**
- Two values are at the same position
- Example: The Brit lives in the red house
- Parameters: Category 1, Value 1, Category 2, Value 2

**Adjacent**
- Two values are next to each other
- Example: The snail owner lives next to the tea drinker
- Parameters: Category 1, Value 1, Category 2, Value 2

**Immediately Right Of**
- One value is exactly one position to the right of another
- Example: The green house is immediately to the right of the red house
- Parameters: Category 1 (right), Value 1, Category 2 (left), Value 2

**Left Of**
- One value is somewhere to the left of another
- Example: The red house is to the left of the green house
- Parameters: Category 1 (left), Value 1, Category 2 (right), Value 2

**At Position**
- A value is at a specific position (0-indexed)
- Example: The Norwegian lives in the first house (position 0)
- Parameters: Category, Value, Position (0 for first, 1 for second, etc.)

**Middle Position**
- A value is in the middle position (works only with odd number of positions)
- Example: Milk is drunk in the middle house
- Parameters: Category, Value, Total Positions

**Not Same Position**
- Two values are NOT at the same position
- Example: The water drinker doesn't live in the red house
- Parameters: Category 1, Value 1, Category 2, Value 2

#### Step 4: Solve
Click **"Solve Puzzle"** and wait for the solution to appear in a table format!

## Example: Creating a Simple 3-House Puzzle

### Setup
```
Number of Positions: 3

Categories:
- nationality: English,Spanish,Japanese
- color: red,green,ivory
- pet: dog,snail,fox
- drink: coffee,tea,water
```

### Constraints
1. Type: Same Position
   - nationality, English, color, red
   - "The Englishman lives in the red house"

2. Type: Same Position
   - nationality, Spanish, pet, dog
   - "The Spaniard owns the dog"

3. Type: Same Position
   - drink, coffee, color, green
   - "Coffee is drunk in the green house"

4. Type: Immediately Right Of
   - color, green, color, red
   - "The green house is immediately to the right of the red house"

5. Type: Adjacent
   - pet, snail, drink, tea
   - "The snail owner lives next to the tea drinker"

6. Type: Adjacent
   - nationality, Japanese, pet, snail
   - "The Japanese lives next to the snail owner"

### Expected Solution
```
Position 1: Japanese, ivory, fox, tea
Position 2: English, red, snail, water
Position 3: Spanish, green, dog, coffee
```

## Tips for Creating Good Puzzles

1. **Unique Solution**: Make sure your constraints lead to exactly one solution
2. **Sufficient Constraints**: Too few constraints = multiple solutions
3. **Consistent Constraints**: Avoid contradictory clues
4. **Start Simple**: Begin with 3 positions and 3-4 categories
5. **Test Incrementally**: Add constraints one at a time and test

## Troubleshooting

### "No solution found"
- Check that constraints are not contradictory
- Ensure category values match the number of positions
- Verify all constraint parameters are correct

### Slow solving
- Puzzles with 5+ positions and 5+ categories may take a few seconds
- This is normal for complex constraint satisfaction problems

### Server not starting
- Check if port 5000 is already in use
- Make sure Flask is installed: `pip install Flask`

## Command-Line Usage

You can also run puzzles from the command line:

```bash
# Run the 3-house example
python3 example_puzzle.py

# Run the classic Einstein puzzle
python3 einstein_puzzle.py
```

## API Usage

You can also use the API directly:

```bash
curl -X POST http://localhost:5001/solve \
  -H "Content-Type: application/json" \
  -d @puzzle.json
```

Where `puzzle.json` contains your puzzle definition.

Get presets:
```bash
curl http://localhost:5001/presets
```
