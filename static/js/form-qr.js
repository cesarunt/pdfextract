// Voucher number
_index = 0
// Length of data
_data_len = 0
// width and height
var div_image
var div_canvasClass
var canvas_width
var canvas_height
var canvas_center
var select_control
var processPDF_wrapper = document.getElementById("processPDF_wrapper");

// ---------------------------
function showAlertPage(message, alert) {
  alert_wrapper.innerHTML = `
    <div id="alert_page" style="padding: 0.5rem 1rem;" class="alert alert-${alert} alert-dismissible fade show" role="alert" style="line-height:15px;">
      <small>${message}</small>
    </div>
  `
  setTimeout(function () {
    // Closing the alert
    $('#alert_page').alert('close');
  }, 5000);
}

// Function to Show Progress QR
function clicQRProgress(_this) {
  // Reject if the file input is empty & throw alert
  // if (!inputPDF.value) {
  //   showPDFAlert("Seleccione un archivo PDF", "warning")
  //   return;
  // }
  // Hide the Cancel button
  _this.classList.add("d-none");
  // Show the load icon Process
  processPDF_wrapper.classList.remove("d-none");
}

// ACTIVATE ZOOM FUNCTION
function activeZoom(_this, measure, index) {
  var close_zoom = _this.parentNode.querySelector('#close_zoom');
  div_modal = document.getElementById("exampleModal_"+index)
  div_image = div_modal.querySelector('#div_image');
  div_canvasId = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").querySelector("#canvas")
  div_canvasClass = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").querySelector(".upper-canvas")
  div_image.style.border = "2px dotted gray";
  if (measure=='H'){
    // div_canvasId.style.transform = "scale(1.7) translate(-25px, -25px)";
    // div_canvasClass.style.transform = "scale(1.7) translate(-25px, -25px)";
    div_image.classList.add("measure_h");
  }
  else {
    div_image.classList.add("measure_w");
  }
  close_zoom.style.opacity = 1.0;
  close_zoom.disabled = false
  _this.disabled = true
}

// DEACTIVATE ZOOM FUNCTION
function closeZoom(_this, measure) {
  var btn_zoom = _this.parentNode.querySelector('#btn_zoom');
  div_image.style.border = "0";
  if (measure=='H'){
    div_image.classList.remove("measure_h");
    div_canvasId.style.transform = "scale(1.0)";
    div_canvasClass.style.transform = "scale(1.0)";
  }
  else {
    div_image.classList.remove("measure_w");
  }
  btn_zoom.disabled = false
  _this.disabled = true
  _this.style.opacity = 0.5;
}

// --------------------------------------------------------------------------------------------------------
function saveVoucher(_this, url, index) {
  console.log("save Voucher")
  var data_dat = _this.parentNode.parentNode.querySelector('#data_dat')
  var data_cur = _this.parentNode.parentNode.querySelector('#data_cur')
  var data_type = _this.parentNode.parentNode.querySelector('#data_type')
  var data_bill = _this.parentNode.parentNode.querySelector('#data_bill')
  var data_ciaruc = _this.parentNode.parentNode.querySelector('#data_ciaruc')
  var data_cliruc = _this.parentNode.parentNode.querySelector('#data_cliruc')
  var data_tot = _this.parentNode.parentNode.querySelector('#data_tot')
  var data_igv = _this.parentNode.parentNode.querySelector('#data_igv')

  // Reject if the file input is empty & throw alert
  if (!data_dat.value) { alert("Debe ingresar fecha", "warning"); return; }
  if (!data_cur.value) { alert("Debe ingresar moneda", "warning"); return; }
  if (!data_type.value) { alert("Debe ingresar tipo DOC", "warning"); return; }
  if (!data_bill.value) { alert("Debe ingresar No DOC", "warning"); return; }
  if (!data_ciaruc.value) { alert("Debe ingresar RUC empresa", "warning"); return; }
  if (!data_cliruc.value) { alert("Debe ingresar RUC cliente", "warning"); return; }
  if (!data_tot.value) { alert("Debe ingresar total", "warning"); return; }
  if (!data_igv.value) { alert("Debe ingresar IGV", "warning"); return; }

  // Create a new FormData instance
  var data = new FormData();
  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();
  // Set the response type
  request.responseType = "json";

  var action = "save_voucher";
  data.append("action", action);
  data.append("index", index)
  data.append("data_dat", data_dat.value);
  data.append("data_cur", data_cur.value);
  data.append("data_type", data_type.value);
  data.append("data_bill", data_bill.value);
  data.append("data_ciaruc", data_ciaruc.value);
  data.append("data_cliruc", data_cliruc.value);
  data.append("data_tot", data_tot.value);
  data.append("data_igv", data_igv.value);

  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      showAlertPage('Voucher registrado con éxito', 'success')
      location.reload();
    }
    else {
      showAlertPage('Voucher no fue registrado', 'warning')
    }
    if (request.status == 300) {
      showAlertPage(`${request.response.message}`, 'warning')
    }
  });

  // request error handler
  request.addEventListener("error", function (e) {
    showAlertPage('Error registrando voucher', 'danger')
  });
  // Open and send the request
  request.open("POST", url);
  request.send(data);
}

var canvas;
var arrow;
var ctx;

// ACTION in order to OPEN voucher details
function openVoucher(_this, index, data_len, center_w) {
  _index = index
  _data_len = data_len
  canvas_center = center_w
  div_modal = document.getElementById("exampleModal_"+index)
  div_canvasId = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").querySelector("#canvas")
  if (!div_canvasClass){
    canvas_width = div_canvasId.width
    canvas_height = div_canvasId.height
  }
  else{
    div_canvasClass.remove()
  }

  canvas = new fabric.Canvas(div_canvasId);
  arrow = new Rectangle(canvas);
  ctx = canvas.getContext("2d");
  // div_canvasClass = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").querySelector(".upper-canvas")
  div_canvasClass = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").getElementsByClassName("upper-canvas")[0]
  div_canvasId.style.left = center_w
  div_canvasId.width = canvas_width
  div_canvasId.height = canvas_height
  div_canvasClass.style.left = center_w
  div_canvasClass.width = canvas_width
  div_canvasClass.height = canvas_height
}

// ACTION in order to CLOSE voucher details
function closeVoucher(index) {
  // console.log("Close Voucher !!!")
  document.getElementById("exampleModal_"+index).classList.remove("show");
  document.getElementById("exampleModal_"+index).setAttribute("style", `display: `);
  const elements = document.getElementsByClassName("modal-backdrop");
  while (elements.length > 0) elements[0].remove();
}

// ACTION in order to MOVE voucher down & up
function moveVoucher(_this, index, direct) {
  // console.log("Move Voucher !!!")
  if (parseInt(index) >= 0 && parseInt(index) <= parseInt(_data_len)+1){
    if (direct == "up"){
      _index = (parseInt(index) + 1).toString()
    }
    if (direct == "down"){
      _index = (parseInt(index) - 1).toString()
    }
  }
  // canvas = null

  if (parseInt(_index) > 0 && parseInt(_index) < parseInt(_data_len)+1){
    // console.log("I:"+index+" - _I:"+_index + " L:"+_data_len)
    document.getElementById("exampleModal_"+index).classList.remove("show");
    document.getElementById("exampleModal_"+index).setAttribute("style", `display: `);
    // cleanCanvas(canvas);
    // canvas = null
    div_canvasClass.remove()

    div_modal = document.getElementById("exampleModal_"+_index)
    div_canvasId = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").querySelector("#canvas")
    canvas_width = div_canvasId.width
    canvas_height = div_canvasId.height
    
    canvas = new fabric.Canvas(div_canvasId);
    arrow = new Rectangle(canvas);
    ctx = canvas.getContext("2d");
    div_canvasClass = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").getElementsByClassName("upper-canvas")[0]
    // 
    center_width = (740 - canvas_width) / 2
    console.log(center_width)
    div_canvasId.style.left = center_width + "px"
    div_canvasId.width = canvas_width
    div_canvasId.height = canvas_height
    div_canvasClass.style.left = center_width + "px"
    div_canvasClass.width = canvas_width
    div_canvasClass.height = canvas_height
    
    // div_canvasClass = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").querySelector(".upper-canvas")
    // console.log(div_canvasClass)

    // var canvas = new fabric.Canvas(div_canvas);
    // var arrow = new Rectangle(canvas);
    // ctx = canvas.getContext("2d");
    div_modal.classList.add("show");
    div_modal.setAttribute("style", `display: block`);
  }
}