// Get a reference to the progress bar, wrapper & status label
var progressPDF = document.getElementById("progressPDF");
var progressPDF_status = document.getElementById("progressPDF_status");

// Get a reference to the 3 buttons
var uploadPDF_btn = document.getElementById("uploadPDF_btn");
var loadingPDF_btn = document.getElementById("loadingPDF_btn");
var cancelPDF_btn = document.getElementById("cancelPDF_btn");
var thumbnails_tab = document.getElementById("pills-tabContent");

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
var full_pages = document.getElementById('canvas_page')
var _page = 1
var _page_pos = 0
var _pages_text = ""
var _canvas_page = 0
var _band_page = false

// Get a reference to the alert wrapper
var alert_wrapper = document.getElementById("alert_wrapper");

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
  // Hide filters and thumbnails
  thumbnails_tab.classList.add("d-none");
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
  document.getElementById("process").value = '1';
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
function selectPage(val, pages_text, pdf_id) {
  document.getElementById('btn_arrow_left').disabled = false
  document.getElementById('btn_arrow_right').disabled = false
  if (val == 1){
    document.getElementById('btn_arrow_left').disabled = true
  }
  if (val == pages.value){
    document.getElementById('btn_arrow_right').disabled = true
  }
  
  let pages_list = pages_text.split(",")
  _page_pos = pages_list.indexOf((val-1).toString())
  _pages_text = pages_text
  document.getElementById('current_page').value = (val).toString();
  document.getElementById('pages_pos').value = ""
  goPage(parseInt(val), pdf_id)
}

// Ya esta el select, ahora falta el Move ...
// MOVE PAGE FUNCTION, to move inside One PDF
function movePage(_this, pages_text, pdf_id, direct) {
  document.getElementById('btn_arrow_left').disabled = false
  document.getElementById('btn_arrow_right').disabled = false
  var pages_pos = document.getElementById('pages_pos').value
  if (pages_pos!=""){
    document.getElementById('pages_pos').value = ""
    _page_pos = parseInt(pages_pos);
  }
  
  let pages_list = pages_text.split(",")
  
  if (direct == "up"){
    _page_pos = _page_pos + 1
    if (_page_pos == pages_list.length-1){
      _this.disabled = true
    }
    val = pages_list[_page_pos]
  }
  if (direct == "down"){
    _page_pos = _page_pos - 1
    if (_page_pos == 0){
      _this.disabled = true
    }
    val = pages_list[_page_pos]
  }
  if (direct == "set"){
    val = parseInt(_page)
    _page_pos = pages_list.indexOf((val).toString())
    
    if (_page_pos == 0){
      document.getElementById('btn_arrow_left').disabled = true
    }
    if (_page_pos == pages_list.length-1){
      document.getElementById('btn_arrow_right').disabled = true
    }
  }
  
  // clear the canvas
  canvas.clear();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  document.getElementById('current_page').value = val;
  if (_page_pos >= 0 && _page_pos < pages_list.length){
    goPage(val, pdf_id);
  }
}

// SELECT PAGE FUNCTION
function goPage(val, pdf_id) {
  path_page = 'files/split_img/'+pdf_id.toString()+'page_' + (val-1).toString() + '.jpg'
  $("canvas").css("background-image", "url("+path_page+")");
  _page = val
}

// -----------------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------------

// OPEN AND CLOSE PAGE FUNCTION
function openPage(_this, pdf_path, _pdf_id, _i) {
  // path_page = pdf_path + (_i).toString() + '.jpg'
  // $("canvas").css("background-image", "url("+path_page+")");

  val = parseInt(_i)
  head_page = "head_page_" + (_pdf_id).toString() + "_" + (_i).toString()
  // document.getElementById(head_page).value = (val).toString();
  foot_page = "foot_page_" + (_pdf_id).toString() + "_" + (_i).toString()
  // document.getElementById(foot_page).innerHTML = `&nbsp;Pag. ${(val+1).toString()}&nbsp;`;
  goPages(parseInt(val), pdf_path)
  
  page = "page_" + _pdf_id + "_" + _i
  full_page = "full_page_" + _pdf_id + "_" + _i
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

function checkAll(_this, _pdf_id) {
  // console.log("checkAll");
  var checkboxes = document.getElementsByName('page');
  var all_page = "allpage_" + _pdf_id;
  var all_check = document.getElementById(all_page).checked;
  var check_val

  if (all_check == true) { check_val = true; }
  else { check_val = false; }

  for (var checkbox of checkboxes) {
    let mycheck = checkbox.value.split("_");
    if (parseInt(mycheck[1])>1 && _pdf_id==mycheck[0]){
      var mypage = "page_" + checkbox.value;
      document.getElementById(mypage).checked = check_val;
    }
  }
}

// MOVE AND GO PAGE FUNCTION, to move outside One PDF
function movePages(_this, pdf_path, _pdf_id, _i, _pages, direct) {
  if (_canvas_page == 0 && _band_page == false){
    _canvas_page = _i
    _band_page = true
  }
  head_page = "head_page_" + (_pdf_id).toString() + "_" + (_i).toString()
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
  full_page = "full_page_" + _pdf_id + "_" + _i
  check = document.getElementById(page).checked;
  if (check==true){
    document.getElementById(full_page).checked = true;
  }
  else{
    document.getElementById(full_page).checked = false;
  }
}

function goPages(val, pdf_path) {
  document.getElementById(head_page).value = (val).toString();
  document.getElementById(foot_page).innerHTML = `&nbsp;Pag. ${(val+1).toString()}&nbsp;`;
  path_page = pdf_path + (val).toString() + '.jpg'
  $("canvas").css("background-image", "url("+path_page+")");
}

// Function to set current page on keypress
var current_page = document.getElementById("current_page");
if (current_page) {
  current_page.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      var select_page = "page_" + document.getElementById('select_page').value
      _page = document.getElementById("current_page").value;
      document.getElementById(select_page).value = _page
      // Cancel the default action, if needed
      event.preventDefault();
      _pages_text = document.getElementById('pages_text').value
      movePage(this, _pages_text, parseInt(current_page.name), "set");
    }
  });
}

function selectPages(_val, _pdf_id, pdf_path) {
  document.getElementById('btn_arrow_left').disabled = false
  document.getElementById('btn_arrow_right').disabled = false
  if (_val == 1){
    document.getElementById('btn_arrow_left').disabled = true
  }
  if (_val == full_pages.value){
    document.getElementById('btn_arrow_right').disabled = true
  }
  
  page = "page_" + _pdf_id + "_" + _val
  full_page = "full_page_" + _pdf_id + "_" + _canvas_page
  check = document.getElementById(page).checked;
  if (check==true){
    document.getElementById(full_page).checked = true;
  }
  else{
    document.getElementById(full_page).checked = false;
  }

  val = parseInt(_val)
  _canvas_page = val
  goPages(parseInt(val), pdf_path)
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
  document.getElementById('pdf_id_' + pdf_id + '_li').remove();
  document.getElementById('page_' + pdf_id + '_tab').remove();
}

if (document.querySelector('.form-select')){
  const selectElement = document.querySelector('.form-select');

  selectElement.addEventListener('change', (event) => {
    var type_url = document.getElementById("type_url");
    var type_pro = document.getElementById("type_pro");
    var type_doc = document.getElementById("type_doc");

    // Create a new FormData instance
    var data = new FormData();
    // Create a XMLHTTPRequest instance
    var request = new XMLHttpRequest();

    // Set the response type
    request.responseType = "json";

    var action = "list_by_doc";
    data.append("action", action);
    data.append("pro_id", type_pro.value);
    data.append("type_doc", type_doc.value);

    // request load handler (transfer complete)
    request.addEventListener("load", function (e) {
      if (request.status == 200) {
        console.log("Listado OK")
        location.reload();
      }
      else {
        showAlertPage('Listando PDFs', 'warning')
      }
      if (request.status == 300) {
        showAlertPage(`${request.response.message}`, 'warning')
      }
      
    });

    // request error handler
    request.addEventListener("error", function (e) {
      showAlertPage('Error listando PDFs', 'danger')
    });

    // Open and send the request
    request.open("POST", type_url.value);
    request.send(data);

  });
}

function delPDFOne(pdf_len) {

  if (pdf_len==1){
    alert('No se puede eliminar el único PDF de este proyecto')
  }
}

function delPDFAll(url, pro_id, pdf_name, pdf_detid) {

  if (confirm('Desea eliminar el PDF? \n' + pdf_name)) {
    // Create a new FormData instance
    var data = new FormData();
    // Create a XMLHTTPRequest instance
    var request = new XMLHttpRequest();

    // Set the response type
    request.responseType = "json";

    var action = "remove_pdf";
    data.append("action", action);
    data.append("pro_id", pro_id);
    data.append("pdf_detid", pdf_detid);

    // request load handler (transfer complete)
    request.addEventListener("load", function (e) {
      if (request.status == 200) {
        /// Disabled updated button (blue color), and opacity 1
        // alert(`Eliminación Exitosa`, "success");
        showAlertPage('PDF eliminado con éxito', 'success')
        location.reload();
      }
      else {
        // alert(`Alerta en eliminación`, "warning");
        showAlertPage('PDF no fue eliminado', 'warning')
      }
      if (request.status == 300) {
        // alert(`${request.response.message}`, "warning");
        showAlertPage(`${request.response.message}`, 'warning')
      }
    });

    // request error handler
    request.addEventListener("error", function (e) {
      // alert(`Error eliminando el atributo`, "danger");
      showAlertPage('Error eliminando PDF', 'danger')
    });

    // Open and send the request
    request.open("POST", url);
    request.send(data);
  }
}

function editPDFAll(url, pro_id, pdf_type, pdf_nation, pdf_detid) {

  if (pdf_type=="A"){
    pdf_from = "Antecedentes"
    pdf_to = "Marco Teórico"
    pdf_dettype = "M"
  }
  else{
    pdf_from = "Marco Teórico"
    pdf_to = "Antecedentes"
    pdf_dettype = "A"
  }

  if (confirm('Al cambiar se borran los atributos propios de ' + pdf_from + '\nDesea cambiar el PDF, de ' + pdf_from + " a " + pdf_to + ' ?')) {
    // Save it!
    // Create a new FormData instance
    var data = new FormData();
    // Create a XMLHTTPRequest instance
    var request = new XMLHttpRequest();

    // Set the response type
    request.responseType = "json";

    var action = "edit_pdf";
    data.append("action", action);
    data.append("pro_id", pro_id);
    data.append("pdf_detid", pdf_detid);
    data.append("pdf_dettype", pdf_dettype);
    data.append("pdf_detnation", pdf_nation);

    // request load handler (transfer complete)
    request.addEventListener("load", function (e) {
      for (const node of nodes)
        if (node.innerText.toLowerCase().includes(this.value.toLowerCase()))
            node.classList.remove('hidden');
        else
            node.classList.add('hidden');

      if (request.status == 200) {
        showAlertPage('PDF actualizado correctamente', 'success');
        location.reload();
      }
      else {
        showAlertPage('PDF no fue actualizado', 'warning');
      }
      if (request.status == 300) {
        showAlertPage(`${request.response.message}`, 'warning');
      }
    });

    // request error handler
    request.addEventListener("error", function (e) {
      showAlertPage('Error actualizando PDF', 'danger')
    });

    // Open and send the request
    request.open("POST", url);
    request.send(data);
  }
}

// DOUBLE PDF
function doublePDFAll(url, pro_id, pdf_name, pdf_type, pdf_detid) {

  if (confirm('Desea duplicar el PDF? \n' + pdf_name)) {
    // Save it!
    // Create a new FormData instance
    var data = new FormData();
    // Create a XMLHTTPRequest instance
    var request = new XMLHttpRequest();
    // Set the response type
    request.responseType = "json";

    var action = "double_pdf";
    data.append("action", action);
    data.append("pro_id", pro_id);
    data.append("pdf_detid", pdf_detid);
    data.append("pdf_dettype", pdf_type);

    // request load handler (transfer complete)
    request.addEventListener("load", function (e) {
      if (request.status == 200) {
        location.reload();
        showAlertPage('PDF duplicado correctamente', 'success')
      }
      else {
        showAlertPage('PDF no fue duplicado', 'warning')
      }
      if (request.status == 300) {
        showAlertPage(`${request.response.message}`, 'warning')
      }
    });

    // request error handler
    request.addEventListener("error", function (e) {
      showAlertPage('Error duplicando PDF', 'danger')
    });

    // Open and send the request
    request.open("POST", url);
    request.send(data);
  }
}

// SAVE NATION
function saveNation(url, pro_id, pdf_name, pdf_nation,  pdf_detid) {

  if (confirm('Desea cambiar la nacionalidad del PDF? \n' + pdf_name)) {
    // Save it!
    // Create a new FormData instance
    var data = new FormData();
    // Create a XMLHTTPRequest instance
    var request = new XMLHttpRequest();
    // Set the response type
    request.responseType = "json";

    var action = "nation_pdf";
    data.append("action", action);
    data.append("pro_id", pro_id);
    data.append("pdf_detid", pdf_detid);
    data.append("pdf_nation", pdf_nation.value);

    // request load handler (transfer complete)
    request.addEventListener("load", function (e) {
      if (request.status == 200) {
        location.reload();
        showAlertPage('PDF actualizado correctamente', 'success')
      }
      else {
        showAlertPage('PDF no fue actualizado', 'warning')
      }
      if (request.status == 300) {
        showAlertPage(`${request.response.message}`, 'warning')
      }
    });

    // request error handler
    request.addEventListener("error", function (e) {
      showAlertPage('Error actualizando PDF', 'danger')
    });

    // Open and send the request
    request.open("POST", url);
    request.send(data);
  }
  else {
    location.reload();
  }
}

// ACTIVE FILTER FOR BACKGROUNDS AND FRAMEWORKS
function activeBack(_this, pdf_id) {
  document.getElementById("filter_frame_"+pdf_id).classList.add("d-none");
  document.getElementById("filter_back_"+pdf_id).classList.remove("d-none");
}

function activeFrame(_this, pdf_id) {
  document.getElementById("filter_back_"+pdf_id).classList.add("d-none");
  document.getElementById("filter_frame_"+pdf_id).classList.remove("d-none");
}
