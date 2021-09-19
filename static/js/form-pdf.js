// Get a reference to the progress bar, wrapper & status label
var progressPDF = document.getElementById("progressPDF");
var progressPDF_wrapper = document.getElementById("progressPDF_wrapper");
var progressPDF_status = document.getElementById("progressPDF_status");

// Get a reference to the 3 buttons
var uploadPDF_btn = document.getElementById("uploadPDF_btn");
var loadingPDF_btn = document.getElementById("loadingPDF_btn");
// var cancelupImage_btn = document.getElementById("cancelupImage_btn");
var cancelPDF_btn  = document.getElementById("cancelPDF_btn");

var processPDF_btn = document.getElementById("processPDF_btn");
var processPDF_wrapper = document.getElementById("processPDF_wrapper");

// Get a reference to the alert wrapper
var alertPDF_wrapper = document.getElementById("alertPDF_wrapper");

// Get a reference to the file input element & input label 
var inputPDF = document.getElementById("file_pdf");
var file_PDF_label = document.getElementById("file_PDF_label");

// Get a reference to the 3 buttons
// var closeImage_btn  = document.getElementById("closeImage_btn");

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
    //   resetPDFUpload();
      // Disable the analytic control
    //   analyticImage_selected.disabled = true;
    //   // Disable the object control
    //   objectImage_selected.disabled = true;
      // Hide the loading button
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