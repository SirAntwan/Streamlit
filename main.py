import streamlit as st
import streamlit.components.v1 as components
import json

# Set the page to wide mode to ensure the full width of the screen is used
st.set_page_config(layout="wide")

# Define the HTML and JavaScript for the drag-and-drop interface
sortable_html = """
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
    <main class="flex-grow-1">
        <div class="container-fluid mt-4">
            <h1 class="mb-4">Survey Builder</h1>
            <div class="row">
                <div class="col-md-3 col-lg-2">
                    <div id="question-types" class="mb-4">
                        <h2>Question Types</h2>
                        <div class="question" draggable="true" data-type="text">Text Question</div>
                        <div class="question" draggable="true" data-type="multiple-choice">Multiple Choice</div>
                        <div class="question" draggable="true" data-type="checkbox">Checkbox</div>
                        <div class="question" draggable="true" data-type="slider">Slider</div>

                        <button id="save-survey" class="btn btn-primary mt-3">Save Survey</button>
                    </div>
                </div>
                <div class="col-md-9 col-lg-10">
                    <div id="survey-area">
                        <h2>Survey Canvas</h2>
                    </div>
                </div>
            </div>

        </div>
    </main>
    <style>
        #question-types,
#survey-area {
    border: 1px solid #dee2e6;
    border-radius: 0.25rem;
    padding: 1rem;
    margin-bottom: 1rem;
}

#question-types {
    background-color: #f8f9fa;
}

.question {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    cursor: move;
}

.question.dragging {
    opacity: 0.5;
}

.question::before {
    content: '⋮';
    margin-right: 0.5rem;
    color: #6c757d;
}

.question input {
    margin-bottom: 10px;
    width: 100%;
}

.input-group {
    display: flex;
    align-items: center;
}

.input-group .form-control {
    margin-right: 10px;
}

/* Styles for delete buttons */
.btn-danger.btn-sm {
    float: right; /* Positioning for question delete button */
}

.btn-danger.btn-sm {
    padding: 0.2rem 0.5rem; /* Padding for option delete button */
}

/* Ensure the main content area takes up remaining vertical space */
main {
    display: flex;
    flex-direction: column;
}

#survey-area {
    flex-grow: 1;
    min-height: 500px; /* Increased for better visibility */
    background-color: #ffffff;
    padding-bottom: 100px; /* Adjust this value for the height of the space you want */
}

/* Responsive adjustments */
@media (max-width: 768px) {
    #question-types {
        margin-bottom: 1rem;
    }
}

.form-check {
    display: flex; /* Use flexbox for better alignment */
    align-items: center; /* Center items vertically */
    margin: 0.5rem 0; /* Adjust margin around checkbox */
}

.form-check-input {
    -webkit-appearance: checkbox; /* Force default checkbox styling for WebKit browsers */
    -moz-appearance: checkbox; /* Force default checkbox styling for Firefox */
    appearance: checkbox; /* Ensure default appearance */
    width: 20px; /* Set a smaller width for the checkbox */
    height: 20px; /* Set a smaller height for the checkbox */
    margin-right: 0.5rem; /* Space between checkbox and label */
}

.form-check-label {
    margin: 0; /* Remove default margins */
    margin-left: 10px; /* Add left margin for more room */
    white-space: nowrap; /* Prevent text wrapping */
    display: inline; /* Ensure label is inline */
}

.form-control-sm {
    width: 100px; /* Set a specific width for the label input */
    margin-right: 10px; /* Space between input and checkbox */
    float: left;

}

.form-check .form-control-sm {
    vertical-align: middle; /* Ensure all elements are vertically aligned */
    margin-bottom: 0; /* Remove any extra margin if applied */
}


/* Align the add button properly and add left margin */
.btn-secondary.btn-sm.mb-2 {
    vertical-align: middle; /* Align with other elements */
    margin-left: 10px; /* Space to the left */
    margin-top: 5px;
    margin-bottom: 0; /* Remove extra bottom margin */
    align-self: center; /* Ensure the button is centered within the flex container */
}
    </style>

    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.14.0/Sortable.min.js"></script>
    <script>
        // Select DOM elements for question types and survey area
const questionTypes = document.getElementById('question-types');
const surveyArea = document.getElementById('survey-area');
let draggedItem = null; // Variable to hold the currently dragged item

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.question:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

// Event listener for when a drag starts on a question type
questionTypes.addEventListener('dragstart', (e) => {
    // Check if the dragged target is a question
    if (e.target.classList.contains('question')) {
        // Store the type of question being dragged in the dataTransfer object
        e.dataTransfer.setData('text/plain', e.target.dataset.type);
    }
});

// Event listener for dragging over the survey area
surveyArea.addEventListener('dragover', (e) => {
    e.preventDefault(); // Prevent default behavior to allow dropping
    const afterElement = getDragAfterElement(surveyArea, e.clientY); // Get the element after which the dragged item will be placed
    const draggable = document.querySelector('.dragging'); // Get the currently dragged element
    if (afterElement == null) {
        // If there is no afterElement, append the dragged item to the end
        surveyArea.appendChild(draggable);
    } else {
        // Otherwise, insert the dragged item before the afterElement
        surveyArea.insertBefore(draggable, afterElement);
    }
});

// Event listener for dropping a question in the survey area
surveyArea.addEventListener('drop', (e) => {
    e.preventDefault(); // Prevent default behavior
    const questionType = e.dataTransfer.getData('text'); // Get the type of question from dataTransfer
    if (questionType) {
        // If a question type exists, create a new question element
        const newQuestion = createQuestion(questionType);
        const afterElement = getDragAfterElement(surveyArea, e.clientY); // Get the element after which the new question will be placed
        if (afterElement == null) {
            // If no afterElement exists, append the new question
            surveyArea.appendChild(newQuestion);
        } else {
            // Otherwise, insert the new question before the afterElement
            surveyArea.insertBefore(newQuestion, afterElement);
        }
    }
});

// Function to create a question element
function createQuestion(type) {
    const question = document.createElement('div'); // Create a div for the question
    question.className = 'question'; // Set class for styling
    question.draggable = true; // Make the question draggable

    const deleteButton = document.createElement('button');
    deleteButton.className = 'btn btn-danger btn-sm';
    deleteButton.textContent = 'Delete';
    deleteButton.addEventListener('click', () => question.remove());

    const questionLabel = document.createElement('strong');
    questionLabel.textContent = `${type.charAt(0).toUpperCase() + type.slice(1)} Question`;

    const questionText = document.createElement('input');
    questionText.type = 'text';
    questionText.placeholder = 'Enter your question here';
    questionText.className = 'form-control mb-2';

    let inputField;
    if (type === 'multiple-choice') {
        inputField = createMultipleChoiceOptions();
    } else if (type === 'checkbox') {
        inputField = createCheckboxOptions();
    } else if (type === 'slider') {
        inputField = createSliderOptions(); // New function for creating slider options
    } else {
        inputField = null; // No extra inputs for text questions
    }

    question.appendChild(questionLabel);
    question.appendChild(deleteButton);
    question.appendChild(questionText);
    if (inputField) {
        question.appendChild(inputField);
    }

    question.addEventListener('dragstart', () => question.classList.add('dragging'));
    question.addEventListener('dragend', () => question.classList.remove('dragging'));

    return question;
}

// Helper function for multiple-choice options
function createMultipleChoiceOptions() {
    const inputField = document.createElement('div');

    function createOptionInput(placeholder) {
        const optionContainer = document.createElement('div');
        optionContainer.className = 'input-group mb-1';

        const optionInput = document.createElement('input');
        optionInput.type = 'text';
        optionInput.placeholder = placeholder;
        optionInput.className = 'form-control';

        const deleteOptionButton = document.createElement('button');
        deleteOptionButton.className = 'btn btn-danger btn-sm';
        deleteOptionButton.textContent = '✖';
        deleteOptionButton.addEventListener('click', () => optionContainer.remove());

        const inputGroupAppend = document.createElement('div');
        inputGroupAppend.className = 'input-group-append';
        inputGroupAppend.appendChild(deleteOptionButton);

        optionContainer.appendChild(optionInput);
        optionContainer.appendChild(inputGroupAppend);

        return optionContainer;
    }

    inputField.appendChild(createOptionInput('Option 1'));
    inputField.appendChild(createOptionInput('Option 2'));

    const addOptionButton = document.createElement('button');
    addOptionButton.className = 'btn btn-secondary btn-sm mb-2';
    addOptionButton.textContent = 'Add Option';
    addOptionButton.addEventListener('click', () => {
        const optionCount = inputField.querySelectorAll('.input-group').length + 1;
        inputField.insertBefore(createOptionInput(`Option ${optionCount}`), addOptionButton);
    });

    inputField.appendChild(addOptionButton);
    return inputField;
}

// Helper function for checkbox options
function createCheckboxOptions() {
    const inputField = document.createElement('div');

    function createCheckboxOption(placeholder) {
        const checkboxContainer = document.createElement('div');
        checkboxContainer.className = 'form-check d-inline-flex align-items-center mb-1';

        const labelInput = document.createElement('input');
        labelInput.type = 'text';
        labelInput.className = 'form-control-sm';
        labelInput.placeholder = placeholder;

        const checkboxInput = document.createElement('input');
        checkboxInput.type = 'checkbox';
        checkboxInput.className = 'form-check-input';
        checkboxInput.style.marginLeft = '10px';

        const deleteOptionButton = document.createElement('button');
        deleteOptionButton.className = 'btn btn-danger btn-sm';
        deleteOptionButton.textContent = '✖';
        deleteOptionButton.addEventListener('click', () => checkboxContainer.remove());

        checkboxContainer.appendChild(labelInput);
        checkboxContainer.appendChild(checkboxInput);
        checkboxContainer.appendChild(deleteOptionButton);

        return checkboxContainer;
    }

    inputField.appendChild(createCheckboxOption('Label 1'));
    inputField.appendChild(createCheckboxOption('Label 2'));

    const addCheckboxButton = document.createElement('button');
    addCheckboxButton.className = 'btn btn-secondary btn-sm mb-2';
    addCheckboxButton.textContent = 'Add Checkbox';
    addCheckboxButton.addEventListener('click', () => {
        const optionCount = inputField.querySelectorAll('.form-check').length + 1;
        inputField.insertBefore(createCheckboxOption(`Label ${optionCount}`), addCheckboxButton);
    });

    inputField.appendChild(addCheckboxButton);
    return inputField;
}

// Helper function for slider options
// Helper function to create slider options
function createSliderOptions() {
    const inputField = document.createElement('div');

    // Create a container for the slider labels
    const sliderLabels = document.createElement('div');
    sliderLabels.className = 'd-flex justify-content-between mb-2';

    // Create input for the left label (Min value)
    const labelLeft = document.createElement('input');
    labelLeft.type = 'text';
    labelLeft.className = 'form-control-sm';
    labelLeft.placeholder = 'Left Label';

    // Create input for the right label (Max value)
    const labelRight = document.createElement('input');
    labelRight.type = 'text';
    labelRight.className = 'form-control-sm';
    labelRight.placeholder = 'Right Label';

    sliderLabels.appendChild(labelLeft);
    sliderLabels.appendChild(labelRight);

    // Add the labels to the input field
    inputField.appendChild(sliderLabels);

    // Create input fields for the min and max values of the slider
    const minMaxContainer = document.createElement('div');
    minMaxContainer.className = 'd-flex justify-content-between mb-2';

    const minValueInput = document.createElement('input');
    minValueInput.type = 'number';
    minValueInput.className = 'form-control-sm';
    minValueInput.placeholder = 'Min Value';
    minValueInput.value = 0; // Default min value

    const maxValueInput = document.createElement('input');
    maxValueInput.type = 'number';
    maxValueInput.className = 'form-control-sm';
    maxValueInput.placeholder = 'Max Value';
    maxValueInput.value = 100; // Default max value

    minMaxContainer.appendChild(minValueInput);
    minMaxContainer.appendChild(maxValueInput);

    inputField.appendChild(minMaxContainer);

    // Create the actual slider input
    const slider = document.createElement('input');
    slider.type = 'range';
    slider.className = 'form-range mb-2';
    slider.min = minValueInput.value; // Set the slider's minimum value
    slider.max = maxValueInput.value; // Set the slider's maximum value

    // Update slider's min and max dynamically when user changes the inputs
    minValueInput.addEventListener('input', () => {
        slider.min = minValueInput.value; // Update the slider's min value
    });

    maxValueInput.addEventListener('input', () => {
        slider.max = maxValueInput.value; // Update the slider's max value
    });

    inputField.appendChild(slider); // Add the slider to the input field

    return inputField;
}


// Function to save the survey as a text file
document.getElementById('save-survey').addEventListener('click', () => {
    const surveyText = buildSurveyText(); // Build the survey text
    downloadSurvey(surveyText); // Trigger download
});

function buildSurveyText() {
    let surveyText = '';

    const questions = document.querySelectorAll('#survey-area .question');
    questions.forEach(question => {
        const questionType = question.querySelector('strong').textContent.replace(' Question', '');
        const questionText = question.querySelector('input[type="text"]').value;

        switch (questionType.toLowerCase()) {
            case 'multiple-choice':
                surveyText += formatMultipleChoiceQuestion(questionText, question);
                break;
            case 'checkbox':
                surveyText += formatCheckboxQuestion(questionText, question);
                break;
            case 'slider':
                surveyText += formatSliderQuestion(questionText, question); // Handle slider
                break;
            case 'text':
                surveyText += formatTextQuestion(questionText);
                break;
            default:
                surveyText += formatGenericQuestion(questionType, questionText);
        }
    });

    return surveyText;
}

function formatMultipleChoiceQuestion(questionText, questionElement) {
    let text = `Multiple-choice\n${questionText}\n`;
    const options = questionElement.querySelectorAll('.input-group .form-control');
    options.forEach(option => {
        const optionText = option.value.trim();
        if (optionText) {
            text += `*${optionText}\n`;
        }
    });
    text += '\n';
    return text;
}

function formatCheckboxQuestion(questionText, questionElement) {
    let text = `Checkbox\n${questionText}\n`;
    const options = questionElement.querySelectorAll('.form-check .form-control-sm');
    options.forEach(option => {
        const optionText = option.value.trim();
        if (optionText) {
            text += `*${optionText}\n`;
        }
    });
    text += '\n';
    return text;
}

// Function to format a slider question for the text output
function formatSliderQuestion(questionText, questionElement) {
    let text = `Slider\n${questionText}\n`;

    const labels = questionElement.querySelectorAll('.form-control-sm');
    const labelLeft = labels[0].value.trim(); // Get left label
    const labelRight = labels[1].value.trim(); // Get right label
    const minValue = labels[2].value.trim(); // Get min value
    const maxValue = labels[3].value.trim(); // Get max value

    // Include the labels and slider range in the output
    text += `*Left: ${labelLeft}\n`;
    text += `*Right: ${labelRight}\n`;
    text += `*Min: ${minValue}\n`;
    text += `*Max: ${maxValue}\n\n`;

    return text; // Return the formatted slider question
}


function formatTextQuestion(questionText) {
    return `Text\n${questionText}\n\n`;
}

function formatGenericQuestion(questionType, questionText) {
    return `${questionType}\n${questionText}\n\n`;
}

// Function to download the survey as a text file
function downloadSurvey(text) {
    const element = document.createElement('a');
    const file = new Blob([text], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = 'survey.txt';
    document.body.appendChild(element);
    element.click();
}

    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
"""

# Render the HTML/JS interface
components.html(sortable_html, height=1000)

# Initialize the session state to store the survey structure if not present
if 'survey_structure' not in st.session_state:
    st.session_state.survey_structure = []

# Function to handle messages from the drag-and-drop interface
def handle_message():
    message = st.experimental_get_query_params().get("canvas_order")
    if message:
        st.session_state.survey_structure = json.loads(message[0])

handle_message()

# Add a button to generate Python code from the current survey structure
if st.button('Generate Python Code'):
    # Function to generate Python code from the survey structure
    def generate_python_code(survey_structure):
        code = '''import streamlit as st\n\n'''
        page_count = 1
        for component in survey_structure:
            if 'Text Question' in component:
                code += f'def page_{page_count}():\n'
                code += f'    st.text_input("Your text question here")\n\n'
            elif 'Multiple Choice (Radio)' in component:
                code += f'def page_{page_count}():\n'
                code += f'    st.radio("Your radio question here", ["Option 1", "Option 2"])\n\n'
            elif 'Slider Question' in component:
                code += f'def page_{page_count}():\n'
                code += f'    st.slider("Your slider question here", 0, 100)\n\n'
            page_count += 1
        return code

    generated_code = generate_python_code(st.session_state.survey_structure)
    
    st.code(generated_code)
