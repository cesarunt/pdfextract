
var update_att = document.getElementById("btn_save_canvas");
// var text_area = document.getElementById("text_area");

var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

// this flage is true when the user is dragging the mouse
var isDown = false;

// calculate where the canvas is on the window
// (used to help calculate mouseX/mouseY)
var $canvas = $("#canvas");
var canvasOffset = $canvas.offset();
var offsetX = canvasOffset.left;
var offsetY = canvasOffset.top;
var scrollX = $canvas.scrollLeft();
var scrollY = $canvas.scrollTop();

// these vars will hold the starting mouse position
var startX;
var startY;
var prevStartX = 0;
var prevStartY = 0;
var prevWidth  = 0;
var prevHeight = 0;

var _det_id = null
var _det_attribute = null
var _det_name = null
var _x = null
var _y = null
var _w = null
var _h = null
var _page = 1

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
  // Abled vector button
  document.getElementById('vector_'+_det_id+'-'+_det_attribute+'-'+_det_name).style.opacity = 1
  // Abled close button
  // document.getElementById('close_'+_det_id+'-'+_det_attribute+'-'+_det_name).style.opacity = 1
  document.getElementById('close_'+_det_id+'-'+_det_attribute+'-'+_det_name).classList.remove("d-none")
  document.getElementById('remove_'+_det_id+'-'+_det_attribute+'-'+_det_name).classList.add("d-none")
  // Abled edit button, opacity 1
  var divtext_area = document.getElementById("divtext_"+_det_name)
  if (divtext_area) {
    divtext_area.classList.remove("d-none");
  }

  // Abled updated button (blue color), and opacity 1
  document.getElementById("btn_save_canvas").disabled = false
  document.getElementById('current_page').innerHTML = (select_att.value).toString()

  if (!select_att.value){
    alert("Debe seleccionar la página")
    goPage(1)
  }
  else {
    goPage(select_att.value)
  }
  loadCanvas()
  // Active values for canvas ...
  var det_x = document.getElementById('det_x-'+_det_name).value
  var det_y = document.getElementById('det_y-'+_det_name).value
  var det_width = document.getElementById('det_width-'+_det_name).value
  var det_height = document.getElementById('det_height-'+_det_name).value

  if (det_x != null && det_y != null) {
    ctx.strokeRect(det_x, det_y, det_width, det_height);
  }
  
}

// CLOSE ATTRIBUTE FUNCTION CANCEL
function closeAttribute(edit_id) {
  // Disabled select option
  let detail_id = edit_id.split("_")
  let detail_edit = detail_id[1].split("-")
  _det_id = detail_edit[0]
  _det_attribute = detail_edit[1]
  _det_name = detail_edit[2]
  var select_att = document.getElementById('page_'+_det_id+'-'+_det_attribute)
  select_att.disabled = true
  select_att.style.border = '1px solid #ced4da'
  // Disabled vector button
  document.getElementById('vector_'+_det_id+'-'+_det_attribute+'-'+_det_name).style.opacity = 0.5
  // Disabled close button
  // document.getElementById('close_'+_det_id+'-'+_det_attribute+'-'+_det_name).style.opacity = 0.5
  document.getElementById('close_'+_det_id+'-'+_det_attribute+'-'+_det_name).classList.add("d-none")
  document.getElementById('remove_'+_det_id+'-'+_det_attribute+'-'+_det_name).classList.remove("d-none")
  // Disabled edit button, opacity 1
  var divtext_area = document.getElementById("divtext_"+_det_name)
  if (divtext_area) {
    divtext_area.classList.add("d-none");
  }

  // Disabled updated button (blue color), and opacity 1
  document.getElementById("btn_save_canvas").disabled = true

  // clear the canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  isDown = false
}

// ADD ATTRIBUTE
function addAttribute(edit_id) {
  // Abled div attribute
  document.getElementById('div_attribute').classList.remove("d-none")
}

// CANCEL ATTRIBUTE
function cancelAttribute(edit_id) {
  // Abled div attribute
  document.getElementById('div_attribute').classList.add("d-none")
  document.getElementById('new_attribute').value = ""
}

// REMOVE ATTRIBUTE
function delAttribute(url, edit_id) {
  // Disabled select option
  let detail_id = edit_id.split("_")
  let detail_edit = detail_id[1].split("-")
  _det_id = detail_edit[0]
  console.log(_det_id)
  
  // Create a new FormData instance
  var data = new FormData();
  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();

  // Set the response type
  request.responseType = "json";

  var action = "remove_attribute";
  data.append("action", action);
  data.append("det_id", _det_id);

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      /// Disabled updated button (blue color), and opacity 1
      // update_att.style.opacity = 0.5;
      update_att.disabled = true
      
      alert(`Eliminación Exitosa`, "success");
      location.reload();
    }
    else {
      alert(`Alerta en eliminación`, "warning");
    }
    if (request.status == 300) {
      alert(`${request.response.message}`, "warning");
    }
    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    alert(`Error eliminando el atributo`, "warning");
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);

}

// --------------------------------------------------------------------------------------------------------
function saveCanvas(url) {
  console.log("saveCanvas")

  // Reject if the file input is empty & throw alert
  if (!_x && !_y) {
    alert("Debe seleccionar texto de la imagen", "warning")
    return;
  }
  console.log(_page)

  // Create a new FormData instance
  var data = new FormData();
  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();

  // Set the response type
  request.responseType = "json";

  var action = "save_canvas";
  data.append("action", action);
  data.append("det_id", _det_id);
  data.append("det_attribute", _det_attribute);
  data.append("x", _x);
  data.append("y", _y);
  data.append("w", _w);
  data.append("h", _h);
  data.append("page", _page);

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      /// Disabled updated button (blue color), and opacity 1
      // update_att.style.opacity = 0.5;
      update_att.disabled = true
      
      alert(`Registro Exitoso`, "success");
      location.reload();
    }
    else {
      alert(`Alerta en registro`, "warning");
    }
    if (request.status == 300) {
      alert(`${request.response.message}`, "warning");
    }
    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    alert(`Error procesando la imagen`, "warning");
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);

}

// --------------------------------------------------------------------------------------------------------
function saveText(url, det_name) {
  console.log("saveText")
  let text = "text_" + det_name
  var text_area = document.getElementById(text)
  console.log(text_area.value)

  // Reject if the file input is empty & throw alert
  if (!text_area.value) {
    alert("Debe ingresar texto", "warning")
    return;
  }

  // Create a new FormData instance
  var data = new FormData();
  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();

  // Set the response type
  request.responseType = "json";
  console.log(_det_id)
  console.log(_det_attribute)

  var action = "save_text";
  data.append("action", action);
  data.append("det_id", _det_id);
  data.append("det_attribute", _det_attribute);
  data.append("det_value", text_area.value);

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      /// Disabled updated button (blue color), and opacity 1
      // update_att.style.opacity = 0.5;
      update_att.disabled = true
      
      alert(`Registro Exitoso`, "success");
      location.reload();
    }
    else {
      alert(`Alerta en registro`, "warning");
    }
    if (request.status == 300) {
      alert(`${request.response.message}`, "warning");
    }
    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    alert(`Error procesando el texto`, "warning");
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);

}

// --------------------------------------------------------------------------------------------------------
function saveAttribute(url) {
  console.log("saveAttribute")
  // let text = "text_" + det_name
  var new_att = document.getElementById('new_attribute')
  console.log(new_att.value)

  // Reject if the file input is empty & throw alert
  if (!new_att.value) {
    alert("Debe ingresar atributo", "warning")
    return;
  }

  // Create a new FormData instance
  var data = new FormData();
  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();

  // Set the response type
  request.responseType = "json";
  console.log(_det_id)
  console.log(_det_attribute)

  var action = "save_attribute";
  data.append("action", action);
  data.append("new_att", new_att.value);

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      /// Disabled updated button (blue color), and opacity 1
      // update_att.style.opacity = 0.5;
      update_att.disabled = true
      
      alert(`Registro Exitoso`, "success");
      location.reload();
    }
    else {
      alert(`Alerta en registro`, "warning");
    }
    if (request.status == 300) {
      alert(`${request.response.message}`, "warning");
    }
    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    alert(`Error procesando el texto`, "warning");
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);

}

// Canvas Functions
// ---------------------------------------------------------------------------------------------------------------------
// get references to the canvas and context
function loadCanvas() {
  // style the context
  ctx.strokeStyle = "blue";
  ctx.lineWidth = 2;

  // listen for mouse events
  $("#canvas").mousedown(function (e) { handleMouseDown(e); });
  $("#canvas").mousemove(function (e) { handleMouseMove(e); });
  $("#canvas").mouseup(function (e)   { handleMouseUp(e);  });
  $("#canvas").mouseout(function (e)  { handleMouseOut(e); });
}

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

  _x = prevStartX;
  _y = prevStartY;
  _w = prevWidth;
  _h = prevHeight;
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

// ---------------------------------------------------------------------------------------------------------------------