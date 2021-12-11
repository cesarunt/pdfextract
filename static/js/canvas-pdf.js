// get references to the canvas and context
var canvas = document.getElementById("canvas_pdf");
var ctx = canvas.getContext("2d");

// style the context
ctx.strokeStyle = "blue";
ctx.lineWidth = 2;

// calculate where the canvas is on the window
// (used to help calculate mouseX/mouseY)
var canvasOffset = canvas.getBoundingClientRect();
var offsetX = canvasOffset.left;
var offsetY = canvasOffset.top;

// this flage is true when the user is dragging the mouse
var isDown = false;

// these vars will hold the starting mouse position
var startX;
var startY;

// var x1 = null
// var x2 = null
// var y1 = null
// var y2 = null

function handleMouseDown(e) {
    console.log('handleMouseDown')
    console.log(e)
    e.preventDefault();
    e.stopPropagation();

    // save the starting x/y of the rectangle
    startX = parseInt(e.clientX - offsetX);
    startY = parseInt(e.clientY - offsetY);

    // set a flag indicating the drag has begun
    isDown = true;
}

function handleMouseUp(e) {
    console.log('handleMouseUp')
    console.log(e)
    e.preventDefault();
    e.stopPropagation();

    // the drag is over, clear the dragging flag
    isDown = false;
    // console.log(x1, x2, y1, y2)
}

function handleMouseOut(e) {
    console.log('handleMouseOut')
    console.log(e)
    e.preventDefault();
    e.stopPropagation();

    // the drag is over, clear the dragging flag
    isDown = false; 
}

function handleMouseMove(e) {
    console.log('handleMouseMove')
    console.log(e)
    e.preventDefault();
    e.stopPropagation();

    // if we're not dragging, just return
    if (!isDown) {
        return;
    }

    // get the current mouse position
    mouseX = parseInt(e.clientX - offsetX);
    mouseY = parseInt(e.clientY - offsetY);

    // Put your mousemove stuff here

    // clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // calculate the rectangle width/height based
    // on starting vs current mouse position
    var width = mouseX - startX;
    var height = mouseY - startY;

    // draw a new rect from the start position 
    // to the current mouse position
    ctx.strokeRect(startX, startY, width, height);
    x1 = startX
    y1 = startY
    x2 = width
    y2 = height
}

document.getElementById('canvas_pdf').addEventListener('mousedown', function(e) {
  handleMouseDown(e);
});
document.getElementById('canvas_pdf').addEventListener('mousemove', function(e) {
  handleMouseMove(e);
});
document.getElementById('canvas_pdf').addEventListener('mouseup', function(e) {
  handleMouseUp(e);
});
document.getElementById('canvas_pdf').addEventListener('mouseout', function(e) {
  handleMouseOut(e);
});

//  codigo ok,