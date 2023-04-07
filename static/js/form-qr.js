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

// Get a reference to the alert wrapper
var item_dataCode = document.getElementById("dataCode");
if (item_dataCode) {
  item_dataCode.innerHTML = ""
}

// Function to show alerts
function show_dataCode(data_code, url) {
  // data = item_dataCode.innerHTML
  console.log("SHOW")
  for(var i = 0; i < data_code.length; i++){
    status_code = data_code[i]['is_full'];
    if (status_code == 1) {
      status_html = '<span class="badge text-dark" style="background-color:rgb(0, 205, 0) !important; padding: 5px 2px;">[100%]</span>'
    }
    if (status_code == 2) {
      status_html = '<span class="badge text-dark" style="background-color:rgb(255, 191, 0) !important; padding: 5px 2px;">[&nbsp;75%]</span>'
    }
    if (status_code == 0) {
      status_html = '<span class="badge text-dark" style="background-color:rgb(150, 150, 150) !important; padding: 5px 2px;">[&nbsp;10%]</span>'
    }
    item_dataCode.innerHTML = item_dataCode.innerHTML + `
        <tr id="data_${data_code[i]['index']}" style="border-bottom: 1px solid #CCC;">
          <td style="text-align: center;">${data_code[i]['index']}</td>
          <td>${data_code[i]['cli_dat']}</td>
          <td style="text-align: center;">${data_code[i]['currency']}</td>
          <td style="text-align: center;">${data_code[i]['type_doc']}</td>
          <td>${data_code[i]['cli_fac']} </td>
          <td>${data_code[i]['cia_ruc']} </td>
          <td>${data_code[i]['cli_ruc']} </td>
          <td style="text-align: center;">${data_code[i]['cli_tot']} </td>
          <td style="text-align: center;">${data_code[i]['cli_igv']} </td>
          <td>
            ${status_html}
          </td>
          <td class="action" style="text-align: center; font-size: medium;">
            <button type="button" class="btn" style="padding: 0 2px;" data-toggle="modal" data-target="#exampleModal_${data_code[i]['index']}" onclick="openVoucher(this, '${data_code[i]['index']}', '${ data_code.length }', '${ data_code[i]['center_w'] }')">
              <span class="fa-fw select-all fas"></span>
            </button>
          </td>
        </tr>
    `
    
    path_code = data_code[i]['path'];
    if (data_code[i]['measure']=='H') {
      path_html = `<div class="mb-6 text-center" id="div_image" style="margin: 0.5rem 0 0 0; width: 99% !important;">
                      <div id="canvasContainer" style="width: 100%; height: auto; margin: 0;">
                          <div id="canvasContainer" class="text-center" style="width: 100%;">
                              <canvas id="canvas" style="background-image: url('${data_code[i]['path']}'); background-size: cover; position: relative; opacity: 0.95; margin: 0 auto; height: '${data_code[i]['measure_h']}' !important; width: '${data_code[i]['measure_w']}'; left: '${data_code[i]['center_w']}';" width='${data_code[i]['measure_w']}' height='${data_code[i]['measure_h']}' left='${data_code[i]['center_w']}'></canvas>
                          </div>
                      </div>
                  </div>`
    }
    else {
      path_html = `<div class="mb-6 text-center" id="div_image" style="margin: 0.5rem 0 0 0; width: 99% !important;">
                      <div id="canvasContainer" style="width: 100%; height: auto; margin: 0;">
                          <div id="canvasContainer" class="text-center" style="width: 100%;">
                              <canvas id="canvas" style="background-image: url('${data_code[i]['path']}'); background-size: cover; position: relative; opacity: 0.95; margin: 0 auto; width: '${data_code[i]['measure_w']}' !important; height: '${data_code[i]['measure_h']}'; left: '${data_code[i]['center_w']}';" width='${data_code[i]['measure_w']}' height='${data_code[i]['measure_h']}' left='${data_code[i]['center_w']}'></canvas>
                          </div>
                      </div>
                  </div>`
    }

    cli_fac_code = data_code[i]['cli_fac'];
    if (cli_fac_code) {
      cli_fac_html = `<input type="text" class="form-control" id="data_bill" name="data_bill" value="${data_code[i]['cli_fac']}" onclick="setValueItem(this, '${data_code[i]['index']}')" required>`
    }
    else {
      cli_fac_html = `<input type="text" class="form-control" id="data_bill" name="data_bill" value="" onclick="setValueItem(this, '${data_code[i]['index']}')" required>`
    }

    cia_ruc_code = data_code[i]['cia_ruc'];
    if (cia_ruc_code) {
      cia_ruc_html = `<input type="text" class="form-control" id="data_cia_ruc" name="data_cia_ruc" value="${data_code[i]['cia_ruc']}" onclick="setValueItem(this, '${data_code[i]['index']}')" required>`
    }
    else {
      cia_ruc_html = `<input type="text" class="form-control" id="data_cia_ruc" name="data_cia_ruc" value="" onclick="setValueItem(this, '${data_code[i]['index']}')" required>`
    }
    cli_ruc_code = data_code[i]['cli_ruc'];
    if (cli_ruc_code) {
      cli_ruc_html = `<input type="text" class="form-control" id="data_cli_ruc" name="data_cli_ruc" value="${data_code[i]['cli_ruc']}" onclick="setValueItem(this, '${data_code[i]['index']}')" required>`
    }
    else {
      cli_ruc_html = `<input type="text" class="form-control" id="data_cli_ruc" name="data_cli_ruc" value="" onclick="setValueItem(this, '${data_code[i]['index']}')" required>`
    }
    cli_tot_code = data_code[i]['cli_tot'];
    if (cli_tot_code) {
      cli_tot_html = `<input type="text" class="form-control" id="data_tot" name="data_tot" value="${data_code[i]['cli_tot']}" onclick="setValueItem(this, '${data_code[i]['index']}')" required>`
    }
    else {
      cli_tot_html = `<input type="text" class="form-control" id="data_tot" name="data_tot" value="" onclick="setValueItem(this, '${data_code[i]['index']}')" required>`
    }
    cli_igv_code = data_code[i]['cli_igv'];
    if (cli_igv_code) {
      cli_igv_html = `<input type="text" class="form-control" id="data_igv" name="data_igv" value="${data_code[i]['cli_igv']}" onclick="setValueItem(this, '${data_code[i]['index']}}')" required>`
    }
    else {
      cli_igv_html = `<input type="text" class="form-control" id="data_igv" name="data_igv" value="" onclick="setValueItem(this, '${data_code[i]['cli_igv']}')" required>`
    }
    cli_status_code = data_code[i]['is_full'];
    if (cli_status_code==1) {
      cli_status_html = `<span class="badge text-dark" style="border: solid 0.35em #EEE; border-left-color: rgb(0, 205, 0); font-size: medium; font-weight: 300;">Completo, por Código QR</span>`
    }
    if (cli_status_code==2) {
      cli_status_html = `<span class="badge text-dark" style="border: solid 0.35em #EEE; border-left-color: rgb(255, 191, 0); font-size: medium; font-weight: 300;">Casi Completo, faltan pocos items</span>`
    }
    if (cli_status_code==0) {
      cli_status_html = `<span class="badge text-dark" style="border: solid 0.35em #EEE; border-left-color: rgb(150, 150, 150); font-size: medium; font-weight: 300;">Incompleto, faltan varios items</span>`
    }

    cli_dat_code = data_code[i]['cli_dat'];
    if (cli_dat_code) {
      cli_dat_html = `<input type="text" class="form-control" id="data_dat" name="data_dat" value="${data_code[i]['cli_dat']}" onclick="setValueItem(this, '${data_code[i]['index']}')" required>`
    }
    else {
      cli_dat_html = `<input type="text" class="form-control" id="data_dat" name="data_dat" value="" onclick="setValueItem(this, `+ data_code[i]['index']+ `)" required> `
    }
    cli_currency_code = data_code[i]['currency'];
    if (cli_currency_code) {
      if (cli_currency_code=="S") {
        cli_currency_html = `<option value="S" selected>Sol</option>
                             <option value="$">Dolar</option>`
      }
      else {
        cli_currency_html = `<option value="S" >Sol</option>
                             <option value="$" selected>Dolar</option>`
      }
    }
    else {
      cli_currency_html = `<option value="S" >Sol</option>
                           <option value="$" >Dolar</option>`
    }

    item_dataCode.innerHTML = item_dataCode.innerHTML + `
          <div class="modal fade" id="exampleModal_${data_code[i]['index']}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div class="modal-dialog" role="document" style="max-width: 1100px;">
              <div class="modal-content" style="background-color: #EEE; width: 1100px;">
                  <div class="modal-body" style="display: inline-flex; top: 5px;">                                                        
                      ${path_html}
                      <div class="mb-4" id="div_items" style="margin: 1.5rem 0.5rem 0 1rem; width: 40%;">
                              <div class="row g-2">
                                  <div class="col-md-6 text-left" style="margin: 1rem 0 0">
                                      <p style="margin: 0 5px 0; color: darkgrey;"><b>VOUCHER &nbsp;${data_code[i]['index']}</b></p>
                                  </div>
                                  <div class="col-md-6" style="text-align: right;">
                                      <button id="arrow_left" type="button" class="btn btn-icon icon-left btn-secondary mb-2" onclick="moveVoucher(this, '${data_code[i]['index']}', 'down')">
                                          <i class="fas fa-arrow-alt-circle-left"></i>
                                      </button>&nbsp;&nbsp;&nbsp;&nbsp;
                                      <button id="arrow_right" type="button" class="btn btn-icon icon-left btn-secondary mb-2" onclick="moveVoucher(this, '${data_code[i]['index']}', 'up')">
                                          <i class="fas fa-arrow-alt-circle-right"></i>
                                      </button>
                                  </div>
                              </div>
                              <div class="line" style="text-align: left; width: 99%; margin: 0.25rem 0 0.75rem; border-color: #999;"></div>
                              <div class="row g-2" style="margin: 0 0 0.75rem;">
                                  <div class="col-md-6" style="text-align: left;">
                                      <button id="btn_zoom" type="button" class="btn btn-icon icon-left btn-info mb-2" onclick="activeZoom(this, '${data_code[i]['measure']}', '${data_code[i]['index']}')">
                                          <i class="fas fa-search-plus"><span> &nbsp;Zoom</span></i>
                                      </button>
                                      <button type="button" id="close_zoom" style="width: 25px; opacity: 0.25;" class="btn btn-icon icon-left btn-secondary mb-2" onclick="closeZoom(this, '${data_code[i]['measure']}')" disabled>
                                          <span class="fa-fw select-all fas" style="margin: 0 -8px;"></span>
                                      </button>
                                  </div>
                                  <div class="col-md-6" style="text-align: center;">
                                      &nbsp;&nbsp;&nbsp;&nbsp;
                                      <button id="btn_extract" type="button" class="btn btn-icon icon-left btn-info mb-2" onclick="getTextCanvas('{{ request.url }}', '${data_code[i]['index']}', '${data_code[i]['path']}')">
                                          <i class="fas fa-sort-alpha-down"><span> &nbsp;Text&nbsp;</span></i>
                                      </button>
                                  </div>
                              </div>
                              <div class="row g-2">
                                  <div class="mb-3 col-md-6">
                                      <p style="margin: 0 5px 0; color: darkgrey;">Fecha</p>
                                      ${cli_dat_html}
                                      <div class="valid-feedback">OK!</div>
                                      <div class="invalid-feedback">Ingrese fecha</div>
                                  </div>
                                  <div class="mb-3 col-md-6">
                                      <p style="margin: 0 5px 0; color: darkgrey;">Moneda</p>
                                      <select id="data_cur" name="data_cur" class="form-select" required>
                                      ${cli_currency_html}
                                      </select>
                                      <div class="valid-feedback">OK!</div>
                                      <div class="invalid-feedback">Seleccione moneda</div>
                                  </div>
                              </div>
                              <div class="row g-2">
                                  <div class="mb-3 col-md-6">
                                      <p style="margin: 0 5px 0; color: darkgrey;">Tipo DOC</p>
                                      <input type="text" class="form-control" id="data_type" name="data_type" value="${data_code[i]['type_doc']}" onclick="setValueItem(this, '${data_code[i]['index']}')" required>
                                      <div class="valid-feedback">OK!</div>
                                      <div class="invalid-feedback">Ingrese tipo</div>
                                  </div>
                                  <div class="mb-3 col-md-6">
                                      <p style="margin: 0 5px 0; color: darkgrey;">Nro Factura</p>
                                      ${cli_fac_html}
                                      <div class="valid-feedback">OK!</div>
                                      <div class="invalid-feedback">Ingrese factura</div>
                                  </div>
                              </div>
                              <div class="row g-2">
                                  <div class="mb-3 col-md-6">
                                      <p style="margin: 0 5px 0; color: darkgrey;">RUC Empresa</p>
                                      ${cia_ruc_html}
                                      <div class="valid-feedback">OK!</div>
                                      <div class="invalid-feedback">Ingrese ruc</div>
                                  </div>
                                  <div class="mb-3 col-md-6">
                                      <p style="margin: 0 5px 0; color: darkgrey;">RUC Cliente</p>
                                      ${cli_ruc_html}
                                      <div class="valid-feedback">OK!</div>
                                      <div class="invalid-feedback">Ingrese ruc</div>
                                  </div>
                              </div>
                              <div class="row g-2">
                                  <div class="mb-3 col-md-6">
                                      <p style="margin: 0 5px 0; color: darkgrey;">Total</p>
                                      ${cli_tot_html}
                                      <div class="valid-feedback">OK!</div>
                                      <div class="invalid-feedback">Ingrese total</div>
                                  </div>
                                  <div class="mb-3 col-md-6">
                                      <p style="margin: 0 5px 0; color: darkgrey;">IGV</p>
                                      ${cli_igv_html}
                                      <div class="valid-feedback">OK!</div>
                                      <div class="invalid-feedback">Ingrese igv</div>
                                  </div>
                              </div>
                              <div class="row g-2">
                                  <div class="mb-12 col-md-12">
                                      <p style="margin: 0 5px 0; color: darkgrey;">Estado <br>
                                      ${cli_status_html}
                                      </p>
                                  </div>
                              </div>
                              <div class="line" style="text-align: left; width: 99%; margin: 0.5rem 0 1.75rem; border-color: #999;"></div>
                              <div class="col-md-12 col-lg-12 text-center" style="margin: 1rem 0 1rem;">
                                  <button type="submit" class="btn btn-primary" onclick="saveVoucher(this, '${url}', '${data_code[i]['index']}')" style="font-size: medium;" > &nbsp; Guardar &nbsp; </button>
                                  <a href="#" onclick="closeVoucher('${data_code[i]['index']}')">
                                      <button type="button" class="btn btn-secondary" style="margin: 0rem; font-size: medium;">&nbsp; Cerrar &nbsp;</button>
                                  </a>
                              </div>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  `
  };
}

// Function to Show Progress QR
function clicQRProgress(_this) {
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

// Function to Process Vouchers by group
function processVouchers(_this, url) {
  var list_vouchers = document.getElementById("list_vouchers");
  url = url + "_action"
  // Hide the Cancel button
  _this.classList.add("d-none");
  // Show the load icon Process
  processPDF_wrapper.classList.remove("d-none");
  
  console.log("process Vouchers")

  // Create a new FormData instance
  var data = new FormData();
  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();
  // Set the response type
  request.responseType = "json";

  var action = "process_vouchers";
  data.append("action", action);
  // data.append("index", index)

  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      list_vouchers.classList.remove("d-none");
      // Hide the load icon Process
      processPDF_wrapper.classList.add("d-none");
      // alert("Voucher registrado con éxito");
      data_code = request.response['data_code'];
      // console.log("data_code");
      // console.log(data_code);
      show_dataCode(data_code, url);
      if (data_code.length>0) {
        request.open("POST", url);
        request.send(data);
        // alert("Vouchers procesados con éxito");
      }
      else {
        console.log("ERROR");
      }
      // alert("Voucher registrado con éxito")
    }
    else {
      alert('Advertencia al cargar', 'warning')
    }
    if (request.status == 300) {
      alert(`${request.response.message}`, 'warning')
    }
  });

  // request error handler
  request.addEventListener("error", function (e) {
    alert('Error registrando voucher', 'danger')
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);
}

// --------------------------------------------------------------------------------------------------------
function saveVoucher(_this, url, index) {
  console.log("save Voucher")
  console.log(url)
  url = url.split("_")
  url = url[0] + "_canvas"
  var data_dat = _this.parentNode.parentNode.querySelector('#data_dat')
  var data_cur = _this.parentNode.parentNode.querySelector('#data_cur')
  var data_type = _this.parentNode.parentNode.querySelector('#data_type')
  var data_bill = _this.parentNode.parentNode.querySelector('#data_bill')
  var data_ciaruc = _this.parentNode.parentNode.querySelector('#data_cia_ruc')
  var data_cliruc = _this.parentNode.parentNode.querySelector('#data_cli_ruc')
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
  data.append("data_cia_ruc", data_ciaruc.value);
  data.append("data_cli_ruc", data_cliruc.value);
  data.append("data_tot", data_tot.value);
  data.append("data_igv", data_igv.value);

  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      // showAlertPage('Voucher registrado con éxito', 'success')
      // location.reload();
      data_code = request.response['data_code'];
      alert("Voucher registrado con éxito")
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
  console.log("Open Voucher")
  _index = index
  _data_len = data_len
  canvas_center = center_w
  div_modal = document.getElementById("exampleModal_"+index)
  // console.log(div_modal)
  div_canvasId = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").querySelector("#canvas")
  // console.log(div_canvasId)
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
  // console.log(div_canvasClass)
  div_canvasId.style.left = center_w
  div_canvasId.width = canvas_width
  div_canvasId.height = canvas_height
  div_canvasClass.style.left = center_w
  div_canvasClass.width = canvas_width
  div_canvasClass.height = canvas_height
}

// ACTION in order to CLOSE voucher details
function closeVoucher(index) {
  document.getElementById("exampleModal_"+index).classList.remove("show");
  document.getElementById("exampleModal_"+index).setAttribute("style", `display: `);
  const elements = document.getElementsByClassName("modal-backdrop");
  while (elements.length > 0) elements[0].remove();
  // location.reload();
}

// ACTION in order to MOVE voucher down & up
function moveVoucher(_this, index, direct) {
  if (parseInt(index) >= 0 && parseInt(index) <= parseInt(_data_len)+1){
    if (direct == "up"){
      _index = (parseInt(index) + 1).toString()
    }
    if (direct == "down"){
      _index = (parseInt(index) - 1).toString()
    }
  }

  if (parseInt(_index) > 0 && parseInt(_index) < parseInt(_data_len)+1){
    // console.log("I:"+index+" - _I:"+_index + " L:"+_data_len)
    document.getElementById("exampleModal_"+index).classList.remove("show");
    document.getElementById("exampleModal_"+index).setAttribute("style", `display: `);
    div_canvasClass.remove()

    div_modal = document.getElementById("exampleModal_"+_index)
    div_canvasId = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").querySelector("#canvas")
    canvas_width = div_canvasId.width
    canvas_height = div_canvasId.height
    
    canvas = new fabric.Canvas(div_canvasId);
    arrow = new Rectangle(canvas);
    ctx = canvas.getContext("2d");
    div_canvasClass = div_modal.querySelector("#canvasContainer").querySelector("#canvasContainer").getElementsByClassName("upper-canvas")[0]
    center_width = (740 - canvas_width) / 2
    console.log(center_width)
    div_canvasId.style.left = center_width + "px"
    div_canvasId.width = canvas_width
    div_canvasId.height = canvas_height
    div_canvasClass.style.left = center_width + "px"
    div_canvasClass.width = canvas_width
    div_canvasClass.height = canvas_height
    div_modal.classList.add("show");
    div_modal.setAttribute("style", `display: block`);
  }
}