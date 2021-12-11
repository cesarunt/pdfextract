// Get a reference to the progress bar, wrapper & status label
var progressPDF = document.getElementById("progressPDF");
var progressPDF_wrapper = document.getElementById("progressPDF_wrapper");
var progressPDF_status = document.getElementById("progressPDF_status");

// Get a reference to the 3 buttons
var uploadPDF_btn = document.getElementById("uploadPDF_btn");
var loadingPDF_btn = document.getElementById("loadingPDF_btn");
var cancelPDF_btn = document.getElementById("cancelPDF_btn");
// var reviewPDF_btn = document.getElementById("reviewPDF_btn")

var processPDF_btn = document.getElementById("processPDF_btn");
var processPDF_wrapper = document.getElementById("processPDF_wrapper");

// Get a reference to the alert wrapper
var alertPDF_wrapper = document.getElementById("alertPDF_wrapper");

// Get a reference to the file input element & input label 
var inputPDF = document.getElementById("file_pdf");
var file_PDF_label = document.getElementById("file_PDF_label");

// Variables for Updating data on thesis_one.html
var select_attributes = document.getElementById("select_attributes");
var updatePDF_btn = document.getElementById("updatePDF_btn");
var div_notfound = document.getElementById("div_notfound");
var div_found = document.getElementById("div_found");


// var iframe_pdf = document.getElementById("iframe_pdf");

// get references to the canvas and context
var canvas_pdf = document.getElementById("canvas_pdf");
var ctx = canvas_pdf.getContext("2d");

// style the context
ctx.strokeStyle = "blue";
ctx.lineWidth = 2;

// calculate where the canvas is on the window
// (used to help calculate mouseX/mouseY)
var canvasOffset = canvas_pdf.getBoundingClientRect();
var offsetX = canvasOffset.left;
var offsetY = canvasOffset.top;

// this flage is true when the user is dragging the mouse
var isDown = false;

// these vars will hold the starting mouse position
var startX;
var startY;

var _x = null
var _y = null
var _w = null
var _h = null

// Canvas Functions
// ---------------------------------------------------------------------------------------------------------------------
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

  console.log(_x, _y, _w, _h)
  // the drag is over, clear the dragging flag
  isDown = false;
}

function handleMouseOut(e) {
  // console.log('handleMouseOut')
  // console.log(e)
  e.preventDefault();
  e.stopPropagation();

  // console.log(_x, _y, _w, _h)
  // the drag is over, clear the dragging flag
  isDown = false; 
}

function handleMouseMove(e) {
  // console.log('handleMouseMove')
  // console.log(e)
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
  ctx.clearRect(0, 0, canvas_pdf.width, canvas_pdf.height);

  // calculate the rectangle width/height based
  // on starting vs current mouse position
  var width = mouseX - startX;
  var height = mouseY - startY;

  // draw a new rect from the start position 
  // to the current mouse position
  ctx.strokeRect(startX, startY, width, height);
  _x = startX
  _y = startY
  _w = width
  _h = height
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

// ---------------------------------------------------------------------------------------------------------------------

// Function to show alerts
function showPDFAlert(message, alert) {
  alertPDF_wrapper.innerHTML = `
    <div id="alertPDF" class="alert alert-${alert} alert-dismissible fade show" role="alert" style="line-height:0.4rem; margin: 1rem 0; text-align: left;">
        <small>${message}</small>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" style="max-height: 0.1rem;"></button>
    </div>
  `  
}

// Function to show content output image
function showPDFResult(imageOut, imageW) {
  // var width = "auto";
  container_postImage.innerHTML = ` 
    <img class="card-img-top" src="${imageOut}" style="border: 1px solid #F55; margin: 0 auto;">
  `
}

// Function to upload file
function clicPDFProcess() {
  // Hide the Cancel button
  cancelPDF_btn.classList.add("d-none");
  // Hide the Process button
  processPDF_btn.classList.add("d-none");
  // Clear any existing alerts
//   alertPDF_wrapper.innerHTML = "";
  // Disable the input during upload
  inputPDF.disabled = true;
  // Show the load icon Process
  processPDF_wrapper.classList.remove("d-none");
}

// Function to upload file
function clicPDFProcessMul() {
  // Hide the Cancel button
  cancelPDF_btn.classList.add("d-none");
  // Hide the Process button
  processPDF_btn.classList.add("d-none");
  // Clear any existing alerts
//   alertPDF_wrapper.innerHTML = "";
  // Show the load icon Process
  processPDF_wrapper.classList.remove("d-none");
}

// Function to upload file ANALYTIC
function uploadPDF(url) {

  // Reject if the file input is empty & throw alert
  if (!inputPDF.value) {
    showPDFAlert("Seleccione un archivo PDF", "warning")
    return;
  }

  // Create a new FormData instance
  var data = new FormData();
  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();

  // Set the response type
  request.responseType = "json";
  // Clear any existing alerts
//   alertPDF_wrapper.innerHTML = "";
  // Disable the input during upload
  inputPDF.disabled = true;
  // reviewPDF_btn.classList.add("d-none");
  // Hide the upload button
  uploadPDF_btn.classList.add("d-none");
  // Show the loading button
  loadingPDF_btn.classList.remove("d-none");
  // Show the progress bar
  progressPDF_wrapper.classList.remove("d-none");

  // Get a reference to the file
  var file = inputPDF.files[0];
  // Get a reference to the filesize & set a cookie
  var filesize = file.size;
//   var process = "image";

  document.cookie = `filesize=${filesize}`;
  // Append the file to the FormData instance
  data.append("file", file);
  // Append identifier of process IMAGE on media value
//   data.append("process", process);

  // request progress handler
  request.upload.addEventListener("progress", function (e) {
    // Get the loaded amount and total filesize (bytes)
    var loaded = e.loaded;
    var total = e.total
    // Calculate percent uploaded
    var percent_complete = (loaded / total) * 100;

    // Update the progress text and progress bar
    progressPDF.setAttribute("style", `width: ${Math.floor(percent_complete)}%`);
    progressPDF_status.innerText = `${Math.floor(percent_complete)}% uploaded`;
  })

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      showPDFAlert(`${request.response.message}`, "success");
      loadingPDF_btn.classList.add("d-none");
      // Hide the progress bar
      progressPDF_wrapper.classList.add("d-none");
      // Show the cancel button
      cancelPDF_btn.classList.remove("d-none");
      // Show the process button
      processPDF_btn.classList.remove("d-none");
    }
    else {
      showPDFAlert(`Error cargando archivo`, "danger");
      resetPDFUpload();
    }

    if (request.status == 300) {
      showPDFAlert(`${request.response.message}`, "warning");
      resetPDFUpload();
    }
    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    resetPDFUpload();
    showPDFAlert(`Error procesando la imagen`, "warning");
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);

}

if(cancelPDF_btn)
{
  cancelPDF_btn.addEventListener("click", function (e) {
    resetImageStart();
  })
}

// Function to update the input placeholder
function input_pdf_file() {
//   file_PDF_label.innerText = inputPDF.files[0].name;
}

// Function to reset the upload
function resetPDFUpload() {
  // Reset the input video element
  inputPDF.disabled = false;
  // Show the upload button
  uploadPDF_btn.classList.remove("d-none");
  // Hide the loading button
  loadingPDF_btn.classList.add("d-none");
  // Hide the progress bar
  progressPDF_wrapper.classList.add("d-none");
  // Reset the progress bar state
  progressPDF.setAttribute("style", `width: 0%`);
}

// Function to reset the page
function resetImageStart() {
  // Clear the input
  inputPDF.value = null;
  inputPDF.disabled = false;
  // Reset the input placeholder
//   file_PDF_label.innerText = "Seleccionar archivo";
  // Hide the cancel button
  cancelPDF_btn.classList.add("d-none");
  // Hide the process button
  processPDF_btn.classList.add("d-none");
  // Hide the alertVideo_wrapper alert
//   alertPDF_wrapper.innerHTML = ``
  // Show the upload button
  uploadPDF_btn.classList.remove("d-none");
}

// Function to select Found or Not-Found attributes from PDF
function on_select_attributes() {
  // Set value to the analytic control
  if (select_attributes.value=="notfound"){
    // Hide the upload button
    div_found.classList.add("d-none");
    // Show the upload button
    div_notfound.classList.remove("d-none");
  }
  if (select_attributes.value=="found"){
    // Hide the upload button
    div_notfound.classList.add("d-none");
    // Show the upload button
    div_found.classList.remove("d-none");
  }
}


// Function to active canvas and hide/show buttons
function activeCanvas(edit_id) {
  canvas_pdf.style.opacity = 1;

  // Hide edit_id
  // Show save_id
  let save_id = "save-"+edit_id.split("-")[1]
  var edit_btn = document.getElementById(edit_id);
  var save_btn = document.getElementById(save_id);
  edit_btn.classList.add("d-none")
  save_btn.classList.remove("d-none");
}

// Function to save over canvas and hide/show buttons
function saveCanvas_(save_id) {
  // Hide save_id
  // Show edit_id
  let edit_id = "edit-"+save_id.split("-")[1]
  var save_btn = document.getElementById(save_id);
  var edit_btn = document.getElementById(edit_id);
  save_btn.classList.add("d-none")
  edit_btn.classList.remove("d-none");

  // Print rectangle values (X,Y, width, heigth)
  console.log("Coordenadas")
  console.log(_x, _y, _w, _h)

}

// --------------------------------------------------------------------------------------------------------
function saveCanvas(url, save_id) {

  // Reject if the file input is empty & throw alert
  if (!_x && !_y) {
    alert("Debe seleccionar texto de la imagen", "warning")
    return;
  }

  // Create a new FormData instance
  var data = new FormData();
  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();

  // Set the response type
  request.responseType = "json";

  var action = "save_attribute";
  data.append("action", action);
  data.append("x", _x);
  data.append("y", _y);
  data.append("w", _w);
  data.append("h", _h);

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      // Hide save_id
      // Show edit_id
      let edit_id = "edit-"+save_id.split("-")[1]
      var save_btn = document.getElementById(save_id);
      var edit_btn = document.getElementById(edit_id);
      save_btn.classList.add("d-none")
      edit_btn.classList.remove("d-none");
      alert(`Registro Exitoso`, "warning");
      canvas_pdf.style.opacity = 0.5;
    }
    else {
      let edit_id = "edit-"+save_id.split("-")[1]
      var save_btn = document.getElementById(save_id);
      var edit_btn = document.getElementById(edit_id);
      save_btn.classList.add("d-none")
      edit_btn.classList.remove("d-none");
      alert(`Registro Exitoso`, "warning");
      canvas_pdf.style.opacity = 0.5;
    }

    if (request.status == 300) {
      alert(`${request.response.message}`, "warning");
    }
    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    // resetImageUpload();
    alert(`Error procesando la imagen`, "warning");
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);

}