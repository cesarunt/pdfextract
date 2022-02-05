// get references to the canvas and context
// var canvas_pdf = document.getElementById("canvas");

// if (canvas_pdf){
//   var ctx = canvas_pdf.getContext("2d");
//   ctx.strokeStyle = "blue";
//   ctx.lineWidth = 2;

//   // calculate where the canvas is on the window
//   // (used to help calculate mouseX/mouseY)
//   var canvasOffset = canvas_pdf.getBoundingClientRect();
//   var offsetX = canvasOffset.left;
//   var offsetY = canvasOffset.top;

//   // this flage is true when the user is dragging the mouse
//   var isDown = false;
//   // these vars will hold the starting mouse position
//   var startX;
//   var startY;
//   // Define global variables
//   var _det_id = null
//   var _det_attribute = null
//   var _det_name = null
//   var _x = null
//   var _y = null
//   var _w = null
//   var _h = null
//   var _page = 1
// }

// ACTIVATE ATTRIBUTE FUNCTION
function activeAttribute(edit_id) {
  // Abled select option
  let detail_id = edit_id.split("_")
  let detail_edit = detail_id[1].split("-")
  _det_id = detail_edit[0]
  _det_attribute = detail_edit[1]
  _det_name = detail_edit[2]
  var select_att = document.getElementById('page_'+_det_id+'-'+_det_attribute)
  select_att.disabled = false
  select_att.style.border = '1px solid #0d6efd'
  // Disabled edit button
  document.getElementById('edit_'+_det_id+'-'+_det_attribute+'-'+_det_name).disabled = true
  // Abled vector button
  document.getElementById('vector_'+_det_id+'-'+_det_attribute+'-'+_det_name).disabled = false
  // Abled updated button (blue color), and opacity 1
  update_att.style.opacity = 1;
  update_att.disabled = false
  // Abled cancel button
  cancel_att.disabled = false

  document.getElementById('current_page').innerHTML = (select_att.value).toString()
  goPage(select_att.value)

  // Active values for canvas ...
  // Verify data x, y

  // var det_x = document.getElementById('det_x-'+_det_name).value
  // var det_y = document.getElementById('det_y-'+_det_name).value
  // var det_width = document.getElementById('det_width-'+_det_name).value
  // var det_height = document.getElementById('det_height-'+_det_name).value

  // if (det_x != null && det_y != null) {
  //   ctx.strokeRect(det_x, det_y, det_width, det_height);
  // }
}

// Canvas Functions
// ---------------------------------------------------------------------------------------------------------------------
// get references to the canvas and context
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

// style the context
ctx.strokeStyle = "blue";
ctx.lineWidth = 2;

// calculate where the canvas is on the window
// (used to help calculate mouseX/mouseY)
var $canvas = $("#canvas");
var canvasOffset = $canvas.offset();
var offsetX = canvasOffset.left;
var offsetY = canvasOffset.top;
var scrollX = $canvas.scrollLeft();
var scrollY = $canvas.scrollTop();

// this flage is true when the user is dragging the mouse
var isDown = false;

// these vars will hold the starting mouse position
var startX;
var startY;

var prevStartX = 0;
var prevStartY = 0;

var prevWidth  = 0;
var prevHeight = 0;

function handleMouseDown(e) {
    e.preventDefault();
    e.stopPropagation();

    // save the starting x/y of the rectangle
    startX = parseInt(e.clientX - offsetX);
    startY = parseInt(e.clientY - offsetY);

    // set a flag indicating the drag has begun
    isDown = true;
}

function handleMouseUp(e) {
    e.preventDefault();
    e.stopPropagation();

    // the drag is over, clear the dragging flag
    isDown = false;
    ctx.strokeRect(prevStartX, prevStartY, prevWidth, prevHeight);
}

function handleMouseOut(e) {
    e.preventDefault();
    e.stopPropagation();

    // the drag is over, clear the dragging flag
    isDown = false;
}

function handleMouseMove(e) {
    e.preventDefault();
    e.stopPropagation();

    // if we're not dragging, just return
    if (!isDown) {
        return;
    }

    // get the current mouse position
    mouseX = parseInt(e.clientX - offsetX);
    mouseY = parseInt(e.clientY - offsetY);

    // calculate the rectangle width/height based
    // on starting vs current mouse position
    var width = mouseX - startX;
    var height = mouseY - startY;

		// clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // draw a new rect from the start position 
    // to the current mouse position
    ctx.strokeRect(startX, startY, width, height);
    
		prevStartX = startX;
		prevStartY = startY;
		prevWidth  = width;
		prevHeight = height;
}

// listen for mouse events
$("#canvas").mousedown(function (e) { handleMouseDown(e); });
$("#canvas").mousemove(function (e) { handleMouseMove(e); });
$("#canvas").mouseup(function (e)   { handleMouseUp(e);  });
$("#canvas").mouseout(function (e)  { handleMouseOut(e); });

// ---------------------------------------------------------------------------------------------------------------------