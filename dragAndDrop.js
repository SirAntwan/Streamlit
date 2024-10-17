// script.js

var itemsEl = document.getElementById('items');
var canvasEl = document.getElementById('canvas');

// Make the components list draggable but not sortable
new Sortable(itemsEl, {
    animation: 150,
    sort: false,  // Disable sorting in the components list
    group: {
        name: 'shared',
        pull: 'clone',  // Allow components to be dragged out but not moved
        put: false      // Prevent dropping back into the original list
    },
});

// Make the canvas list also draggable and sortable
new Sortable(canvasEl, {
    animation: 150,
    group: {
        name: 'shared',  // Enable dragging between lists
        pull: false,     // Disable dragging from the canvas
        put: true        // Allow dropping components into the canvas
    },
    onAdd: function (evt) {
        var newItem = evt.item;
        newItem.id = evt.item.id + '_' + Date.now(); // Unique ID for each new item

        // Ensure it doesn't appear in the original list again
        newItem.style.padding = "10px";
        newItem.style.border = "1px solid #ccc";
        newItem.style.marginBottom = "5px";

        // Add a text box for the Text Question component
        if (newItem.id.startsWith('text_input')) {
            var inputBox = document.createElement('input');
            inputBox.type = 'text';
            inputBox.placeholder = 'Type your question here...';
            inputBox.style.display = 'block';
            inputBox.style.marginTop = '5px';

            newItem.appendChild(inputBox);
        }

        // Send the updated canvas order to Streamlit and adjust canvas height
        updateCanvas();
    },
    onEnd: function () {
        updateCanvas();
    },
});

// Function to send the canvas items back to Streamlit
function updateCanvas() {
    let order = [];
    document.querySelectorAll('#canvas li').forEach(function(el) {
        order.push(el.id);
    });
    
    // Adjust canvas height based on the number of items
    const canvasHeight = Math.max(200, order.length * 60);  // Each item adds 60px to the height
    document.getElementById('canvas').style.minHeight = canvasHeight + 'px';
    
    // Update the iframe height for dynamic resizing in Streamlit
    window.parent.postMessage({height: document.body.scrollHeight}, "*");
    
    window.parent.postMessage({type: 'canvas_order', order: order}, '*');
}

// Set the initial iframe height on load
window.addEventListener('load', function() {
    window.parent.postMessage({height: document.body.scrollHeight}, "*");
});
