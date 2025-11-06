// Global state
let currentPresets = {};

// Load presets from server
async function loadPresets() {
    try {
        const response = await fetch('/presets');
        currentPresets = await response.json();
    } catch (error) {
        console.error('Failed to load presets:', error);
    }
}

// Load a preset puzzle
function loadPreset(presetName) {
    if (!currentPresets[presetName]) {
        alert('Preset not found!');
        return;
    }

    const preset = currentPresets[presetName];

    // Set number of positions
    document.getElementById('numPositions').value = preset.num_positions;

    // Load categories
    const categoriesContainer = document.getElementById('categoriesContainer');
    categoriesContainer.innerHTML = '';

    for (const [categoryName, values] of Object.entries(preset.categories)) {
        const categoryRow = createCategoryRow(categoryName, values.join(','));
        categoriesContainer.appendChild(categoryRow);
    }

    // Load constraints
    const constraintsContainer = document.getElementById('constraintsContainer');
    constraintsContainer.innerHTML = '';

    for (const constraint of preset.constraints) {
        const constraintRow = createConstraintRow(constraint);
        constraintsContainer.appendChild(constraintRow);
    }

    // Show success message
    showMessage('Loaded preset: ' + preset.name, 'success');
}

// Add a new category
function addCategory() {
    const categoriesContainer = document.getElementById('categoriesContainer');
    const categoryRow = createCategoryRow('', '');
    categoriesContainer.appendChild(categoryRow);
}

// Create category row element
function createCategoryRow(name = '', values = '') {
    const div = document.createElement('div');
    div.className = 'category-row';
    div.innerHTML = `
        <input type="text" class="category-name" placeholder="Category name (e.g., color)" value="${name}">
        <input type="text" class="category-values" placeholder="Values (comma-separated)" value="${values}">
        <button class="btn-small btn-danger" onclick="removeCategory(this)">Remove</button>
    `;
    return div;
}

// Remove a category
function removeCategory(button) {
    button.parentElement.remove();
}

// Add a new constraint
function addConstraint() {
    const constraintsContainer = document.getElementById('constraintsContainer');
    const constraintRow = createConstraintRow();
    constraintsContainer.appendChild(constraintRow);
}

// Create constraint row element
function createConstraintRow(constraint = null) {
    const div = document.createElement('div');
    div.className = 'constraint-row';

    const type = constraint ? constraint.type : 'same_position';
    const params = constraint ? constraint.params : [];
    const description = constraint ? constraint.description : '';

    div.innerHTML = `
        <div class="constraint-header">
            <strong>Constraint</strong>
            <button class="btn-small btn-danger" onclick="removeConstraint(this)">Remove</button>
        </div>
        <div class="constraint-type-select">
            <label>Type:</label>
            <select class="constraint-type" onchange="updateConstraintParams(this)">
                <option value="same_position" ${type === 'same_position' ? 'selected' : ''}>Same Position</option>
                <option value="adjacent" ${type === 'adjacent' ? 'selected' : ''}>Adjacent</option>
                <option value="immediately_right_of" ${type === 'immediately_right_of' ? 'selected' : ''}>Immediately Right Of</option>
                <option value="left_of" ${type === 'left_of' ? 'selected' : ''}>Left Of</option>
                <option value="at_position" ${type === 'at_position' ? 'selected' : ''}>At Position</option>
                <option value="middle_position" ${type === 'middle_position' ? 'selected' : ''}>Middle Position</option>
                <option value="not_same_position" ${type === 'not_same_position' ? 'selected' : ''}>Not Same Position</option>
            </select>
        </div>
        <div class="constraint-params">
            ${generateParamInputs(type, params)}
        </div>
        <div class="constraint-description">
            <label>Description:</label>
            <input type="text" class="description-input" placeholder="E.g., The Brit lives in the red house" value="${description}">
        </div>
    `;

    return div;
}

// Generate parameter inputs based on constraint type
function generateParamInputs(type, params = []) {
    const templates = {
        'same_position': [
            { label: 'Category 1', placeholder: 'nationality' },
            { label: 'Value 1', placeholder: 'Brit' },
            { label: 'Category 2', placeholder: 'color' },
            { label: 'Value 2', placeholder: 'red' }
        ],
        'adjacent': [
            { label: 'Category 1', placeholder: 'pet' },
            { label: 'Value 1', placeholder: 'cat' },
            { label: 'Category 2', placeholder: 'drink' },
            { label: 'Value 2', placeholder: 'tea' }
        ],
        'immediately_right_of': [
            { label: 'Category 1 (right)', placeholder: 'color' },
            { label: 'Value 1', placeholder: 'green' },
            { label: 'Category 2 (left)', placeholder: 'color' },
            { label: 'Value 2', placeholder: 'red' }
        ],
        'left_of': [
            { label: 'Category 1 (left)', placeholder: 'color' },
            { label: 'Value 1', placeholder: 'red' },
            { label: 'Category 2 (right)', placeholder: 'color' },
            { label: 'Value 2', placeholder: 'green' }
        ],
        'at_position': [
            { label: 'Category', placeholder: 'nationality' },
            { label: 'Value', placeholder: 'Norwegian' },
            { label: 'Position (0-based)', placeholder: '0', type: 'number' }
        ],
        'middle_position': [
            { label: 'Category', placeholder: 'drink' },
            { label: 'Value', placeholder: 'milk' },
            { label: 'Total Positions', placeholder: '5', type: 'number' }
        ],
        'not_same_position': [
            { label: 'Category 1', placeholder: 'drink' },
            { label: 'Value 1', placeholder: 'water' },
            { label: 'Category 2', placeholder: 'color' },
            { label: 'Value 2', placeholder: 'red' }
        ]
    };

    const template = templates[type] || templates['same_position'];
    return template.map((field, index) => {
        const value = params[index] !== undefined ? params[index] : '';
        const inputType = field.type || 'text';
        return `
            <input type="${inputType}"
                   class="param-input"
                   placeholder="${field.placeholder}"
                   value="${value}"
                   title="${field.label}">
        `;
    }).join('');
}

// Update constraint parameters when type changes
function updateConstraintParams(select) {
    const constraintRow = select.closest('.constraint-row');
    const paramsDiv = constraintRow.querySelector('.constraint-params');
    const type = select.value;
    paramsDiv.innerHTML = generateParamInputs(type);
}

// Remove a constraint
function removeConstraint(button) {
    button.closest('.constraint-row').remove();
}

// Collect puzzle data from form
function collectPuzzleData() {
    const numPositions = parseInt(document.getElementById('numPositions').value);

    // Collect categories
    const categories = {};
    const categoryRows = document.querySelectorAll('.category-row');

    for (const row of categoryRows) {
        const name = row.querySelector('.category-name').value.trim();
        const valuesStr = row.querySelector('.category-values').value.trim();

        if (name && valuesStr) {
            const values = valuesStr.split(',').map(v => v.trim()).filter(v => v);
            if (values.length !== numPositions) {
                throw new Error(`Category "${name}" has ${values.length} values, but ${numPositions} positions specified`);
            }
            categories[name] = values;
        }
    }

    if (Object.keys(categories).length < 2) {
        throw new Error('At least 2 categories are required');
    }

    // Collect constraints
    const constraints = [];
    const constraintRows = document.querySelectorAll('.constraint-row');

    for (const row of constraintRows) {
        const type = row.querySelector('.constraint-type').value;
        const params = Array.from(row.querySelectorAll('.param-input')).map(input => {
            return input.type === 'number' ? parseInt(input.value) : input.value;
        });
        const description = row.querySelector('.description-input').value;

        // Validate params
        if (params.some(p => {
            if (typeof p === 'number') {
                return isNaN(p);
            }
            return p === '' || p === null || p === undefined;
        })) {
            throw new Error('All constraint parameters must be filled');
        }

        constraints.push({ type, params, description });
    }

    if (constraints.length === 0) {
        throw new Error('At least one constraint is required');
    }

    return { num_positions: numPositions, categories, constraints };
}

// Solve the puzzle
async function solvePuzzle() {
    try {
        // Collect data
        const puzzleData = collectPuzzleData();

        // Show solving indicator
        const resultsSection = document.getElementById('resultsSection');
        const solvingIndicator = document.getElementById('solvingIndicator');
        const resultsContainer = document.getElementById('resultsContainer');

        resultsSection.style.display = 'block';
        solvingIndicator.style.display = 'block';
        resultsContainer.innerHTML = '';

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        // Send to server
        const response = await fetch('/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(puzzleData)
        });

        const result = await response.json();

        // Hide solving indicator
        solvingIndicator.style.display = 'none';

        if (result.success) {
            displaySolution(result.solution, result.categories);
        } else {
            displayError(result.error);
        }

    } catch (error) {
        document.getElementById('solvingIndicator').style.display = 'none';
        displayError(error.message);
    }
}

// Display the solution
function displaySolution(solution, categories) {
    const resultsContainer = document.getElementById('resultsContainer');

    let html = '<div class="success-message">Solution found!</div>';
    html += '<table class="solution-table">';

    // Header
    html += '<thead><tr><th>Position</th>';
    for (const category of categories) {
        html += `<th>${category}</th>`;
    }
    html += '</tr></thead><tbody>';

    // Rows
    for (const row of solution) {
        html += `<tr><td><strong>${row.position}</strong></td>`;
        for (const category of categories) {
            html += `<td>${row[category]}</td>`;
        }
        html += '</tr>';
    }

    html += '</tbody></table>';
    resultsContainer.innerHTML = html;
}

// Display an error
function displayError(message) {
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = `<div class="error-message"><strong>Error:</strong> ${message}</div>`;
}

// Show a temporary message
function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
    messageDiv.textContent = message;
    messageDiv.style.position = 'fixed';
    messageDiv.style.top = '20px';
    messageDiv.style.right = '20px';
    messageDiv.style.zIndex = '1000';
    messageDiv.style.minWidth = '300px';

    document.body.appendChild(messageDiv);

    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadPresets();

    // Add initial constraint
    if (document.querySelectorAll('.constraint-row').length === 0) {
        addConstraint();
    }
});
