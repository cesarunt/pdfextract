// Get a reference to the progress bar, wrapper & status label
var progressPDF = document.getElementById("progressPDF");
var progressPDF_status = document.getElementById("progressPDF_status");

// Get a reference to the 3 buttons
var uploadPDF_btn = document.getElementById("uploadPDF_btn");
var loadingPDF_btn = document.getElementById("loadingPDF_btn");
var cancelPDF_btn = document.getElementById("cancelPDF_btn");

var processPDF_btn = document.getElementById("processPDF_btn");
var processPDF_wrapper = document.getElementById("processPDF_wrapper");
var progressPDF_btn = document.getElementById("progressPDF_btn");
var progressPDF_wrapper = document.getElementById("progressPDF_wrapper");

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
var pdfs_remove = "" 

var pages = document.getElementById('num_pages')
var _page = 1
var _canvas_page = 0
var _band_page = false

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
  // Show the load icon Process
  processPDF_wrapper.classList.remove("d-none");
}

// Function to Show Progress file
function clicPDFProgressMul() {
  // Reject if the file input is empty & throw alert
  if (!inputPDF.value) {
    showPDFAlert("Seleccione un archivo PDF", "warning")
    return;
  }
  // Hide the Cancel button
  progressPDF_btn.classList.add("d-none");
  // Show the load icon Process
  progressPDF_wrapper.classList.remove("d-none");
}

// Function to Process Part
function clicProcessPart() {
  // Change value process hidden
  document.getElementById("process").value = '0';
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

  document.cookie = `filesize=${filesize}`;
  // Append the file to the FormData instance
  data.append("file", file);
  
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
  // Hide the cancel button
  cancelPDF_btn.classList.add("d-none");
  // Hide the process button
  processPDF_btn.classList.add("d-none");
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

// SELECT PAGE FUNCTION
function selectPage(val, pdf_id) {
  document.getElementById('btn_arrow_left').disabled = false
  document.getElementById('btn_arrow_right').disabled = false
  if (val == 1){
    document.getElementById('btn_arrow_left').disabled = true
  }
  if (val == pages.value){
    document.getElementById('btn_arrow_right').disabled = true
  }
  document.getElementById('current_page').innerHTML = (parseInt(val)).toString()
  goPage(parseInt(val), pdf_id)
}

// MOVE PAGE FUNCTION, to move inside One PDF
function movePage(_this, pdf_id, direct) {
  document.getElementById('btn_arrow_left').disabled = false
  document.getElementById('btn_arrow_right').disabled = false
  if (direct == "up"){
    val = parseInt(_page) + 1
    if (val == pages.value){
      _this.disabled = true
    }
  }
  if (direct == "down"){
    val = parseInt(_page) - 1
    if (val == 1){
      _this.disabled = true
    }
  }
  if (direct == "set"){
    val = parseInt(_page)
    console.log(val)
    if (val <= 1){
      document.getElementById('btn_arrow_left').disabled = true
    }
    if (val >= pages.value){
      document.getElementById('btn_arrow_right').disabled = true
    }
  }
  // clear the canvas
  canvas.clear();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  document.getElementById('current_page').value = (val).toString();
  if (val >= 1 && val <=pages.value){
    goPage(val, pdf_id);
  }
}

// SELECT PAGE FUNCTION
function goPage(val, pdf_id) {
  path_page = 'files/multiple/split_img/'+pdf_id.toString()+'page_' + (val-1).toString() + '.jpg'
  $("canvas").css("background-image", "url("+path_page+")");
  _page = val
}

// -----------------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------------

// OPEN AND CLOSE PAGE FUNCTION
function openPage(_this, pdf_path, _pdf_id, _i) {
  path_page = pdf_path + (_i).toString() + '.jpg'
  $("canvas").css("background-image", "url("+path_page+")");

  foot_page = "foot_page_" + (_pdf_id).toString() + "_" + (_i).toString()
  val = parseInt(_i) + 1
  document.getElementById(foot_page).innerHTML = `&nbsp;Pag. ${(val).toString()}&nbsp;`;
  
  page = "page_" + _pdf_id + "_" + _i
  full_page = "full_page_" + _pdf_id + "_" + _i
  console.log(full_page)
  check = document.getElementById(page).checked;
  if (check==true){
    document.getElementById(full_page).checked = true;
  }
  else{
    document.getElementById(full_page).checked = false;
  }
  _canvas_page = _i
}

function openCheck(_this, _pdf_id, _i) {
  page = "page_" + _pdf_id + "_" + _canvas_page
  check = _this.checked
  if (check==true){
    document.getElementById(page).checked = true;
  }
  else{
    document.getElementById(page).checked = false;
  }
}

// MOVE AND GO PAGE FUNCTION, to move outside One PDF
function movePages(_this, pdf_path, _pdf_id, _i, _pages, direct) {
  if (_canvas_page == 0 && _band_page == false){
    _canvas_page = _i
    _band_page = true
  }
  foot_page = "foot_page_" + (_pdf_id).toString() + "_" + (_i).toString()
  if (direct == "up"){
    if (_canvas_page < parseInt(_pages)-1){
      _canvas_page = parseInt(_canvas_page) + 1
      goPages(_canvas_page, pdf_path)
    }
  }
  if (direct == "down"){
    if (_canvas_page > 0){
      _canvas_page = parseInt(_canvas_page) - 1
      goPages(_canvas_page, pdf_path)
    }
  }
  if (direct == "set"){
    val = parseInt(_pages)
    console.log(val)
    if (val <= 1){
      document.getElementById('btn_arrow_left').disabled = true
    }
    if (val >= pages.value){
      document.getElementById('btn_arrow_right').disabled = true
    }
    if (val>1 && val<pages.value){
      goPages(_canvas_page, pdf_path);
    }
  }

  page = "page_" + _pdf_id + "_" + _canvas_page
  console.log(page)
  full_page = "full_page_" + _pdf_id + "_" + _i
  console.log(full_page)
  check = document.getElementById(page).checked;
  if (check==true){
    document.getElementById(full_page).checked = true;
  }
  else{
    document.getElementById(full_page).checked = false;
  }

}
function goPages(val, pdf_path) {
  document.getElementById(foot_page).innerHTML = `&nbsp;Pag. ${(val+1).toString()}&nbsp;`;
  path_page = pdf_path + (val).toString() + '.jpg'
  $("canvas").css("background-image", "url("+path_page+")");
}

// Function to set current page on keypress
// function setPage(val)
var current_page = document.getElementById("current_page");
if (current_page) {
  current_page.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      _page = document.getElementById("current_page").value;
      // Cancel the default action, if needed
      event.preventDefault();
      movePage(this, parseInt(current_page.name), "set");
    }
  });
}

var full_current_page = document.getElementById("full_current_page");
if (full_current_page) {
  console.log("full current");
  console.log(full_current_page)
  full_current_page.focus();
  full_current_page.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      _page = document.getElementById("full_current_page").value;
      // Cancel the default action, if needed
      event.preventDefault();
      console.log("OK.......");
      // _pdf_path = document.getElementById("full_path").value;
      // _pdf_id = parseInt(full_current_page.name);
      // _i = document.getElementById("full_i").value;
      // _pages = document.getElementById("full_npages").value;
      // movePages(this, _pdf_path, _pdf_id, _i, _pages, "set");
    }
  });
}

// Function to inactive canvas and hide/show buttons
function cancelCanvas(edit_id) {
  update_att.style.opacity = 0.1
  update_att.disabled = true
  cancel_att.disabled = true
  document.getElementById("cancel_att").disabled = true

  let detail_id = edit_id.split("_")
  let detail_edit = detail_id[1].split("-")
  _det_id = detail_edit[0]
  _det_attribute = detail_edit[1]
  ctx.clearRect(0, 0, canvas_pdf.width, canvas_pdf.height);
}

function removePDF(url, pdf_id, pdf_name) {
  pdfs_remove = pdfs_remove + '/' + pdf_name
  document.getElementById('pdfs_remove').value = pdfs_remove

  pdf_rem_selec = document.getElementById('pdf_id_' + pdf_id)
  pdf_rem_selec.remove();
}