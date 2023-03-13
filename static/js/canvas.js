// Canvas 

// Dictionary for Canvas Multiple
var dictCanvas = [];

// --------------------------------------------------------------------------------------------------------------
var update_att = document.getElementById("btn_save_canvas");
var _det_id = null
var _det_attribute = null
var _det_name = null
var _x = null
var _y = null
var _w = null
var _h = null
var _page = 1

// --------------------------------------------------------------------------------------------------------------
var Rectangle = (function () {
    function Rectangle(canvas) {
        var inst=this;
        this.canvas = canvas;
        this.className= 'Rectangle';
        this.isDrawing = false;
        this.bindEvents();
    }

	Rectangle.prototype.bindEvents = function() {
    var inst = this;
    inst.canvas.on('mouse:down', function(o) {
      inst.onMouseDown(o);
    });
    inst.canvas.on('mouse:move', function(o) {
      inst.onMouseMove(o);
    });
    inst.canvas.on('mouse:up', function(o) {
      inst.onMouseUp(o);
    });
    inst.canvas.on('object:moving', function(o) {
      inst.disable();
    });
  }
    Rectangle.prototype.onMouseUp = function (o) {
      var inst = this;
      inst.disable();

      var pointer = inst.canvas.getPointer(o.e);
      _width  = Math.abs(origX - pointer.x);
      _height = Math.abs(origY - pointer.y);
      _x = parseInt(origX);
      _y = parseInt(origY);
      _w = parseInt(_width);
      _h = parseInt(_height);

      // Load on dictCanvas
      dictPage = {
        'page': _page.toString(),
        'x': _x,
        'y': _y,
        'w': _w,
        'h': _h,
      }
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      dictCanvas.push(dictPage)
      var objects = canvas.getObjects();
      console.log(objects)
    };

    Rectangle.prototype.onMouseMove = function (o) {
      var inst = this;

      if(!inst.isEnable()){ return; }
      var pointer = inst.canvas.getPointer(o.e);
      var activeObj = inst.canvas.getActiveObject();
      activeObj.stroke= 'red',
      activeObj.strokeWidth= 4;
      activeObj.fill = 'transparent';
      activeObj.opacity = 2.0

      if(origX > pointer.x){
          activeObj.set({ left: Math.abs(pointer.x) }); 
      }
      if(origY > pointer.y){
          activeObj.set({ top: Math.abs(pointer.y) });
      }
      activeObj.set({ width: Math.abs(origX - pointer.x) });
      activeObj.set({ height: Math.abs(origY - pointer.y) });
      activeObj.setCoords();
      inst.canvas.renderAll();
    };

    Rectangle.prototype.onMouseDown = function (o) {
      var inst = this;
      inst.enable();
      // inst.disable();

      var pointer = inst.canvas.getPointer(o.e);
      origX = pointer.x;
      origY = pointer.y;

    	var rect = new fabric.Rect({
          left: origX,
          top: origY,
          originX: 'left',
          originY: 'top',
          width: pointer.x-origX,
          height: pointer.y-origY,
          angle: 0,
          transparentCorners: false,
          hasBorders: false,
          hasControls: false
      });
  	  inst.canvas.add(rect).setActiveObject(rect);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    };

    Rectangle.prototype.isEnable = function(){
      return this.isDrawing;
    }

    Rectangle.prototype.enable = function(){
      this.isDrawing = true;
    }

    Rectangle.prototype.disable = function(){
      this.isDrawing = false;
    }

    return Rectangle;
}());

var canvas = new fabric.Canvas('canvas');
var arrow = new Rectangle(canvas);
var ctx = canvas.getContext("2d");


$("canvas").dblclick(function() {
  console.log("cleaning...");
  // ctx.clearRect(0, 0, canvas.width, canvas.height);
  var objects = canvas.getObjects();
  for(var i = 0; i < objects.length; i++){   
    canvas.remove(objects[i]);
  };
  canvas.clear();
  dictCanvas = []
});

// Get a reference to the alert wrapper
var alert_wrapper = document.getElementById("alert_wrapper");

// Function to show alerts
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

// ACTIVATE ATTRIBUTE FUNCTION
function activeAttribute(edit_id, pages_text, pdf_id) {
  // Enabled select option
  let detail_id = edit_id.split("_")
  let detail_edit = detail_id[1].split("-")
  let pages_list = pages_text.split(",")
  _det_id = detail_edit[0]
  _det_attribute = detail_edit[1]
  _det_name = detail_edit[2]
  var select_att = document.getElementById('page_'+_det_id+'-'+_det_attribute)
  select_att.disabled = false
  select_att.style.border = '1px solid #0d6efd'

  // Disabled all controls by name
  var vectors = document.getElementsByName('vectors');
  for (var vector of vectors){
    let vector_id = vector.id
    let get_id = vector_id.split("_")
    document.getElementById("vector_"+get_id[1]).disabled = true;
    document.getElementById("remove_"+get_id[1]).disabled = true;
    document.getElementById("remove_"+get_id[1]).style.opacity = 0.5
  }

  // Enabled vector button
  document.getElementById('vector_'+_det_id+'-'+_det_attribute+'-'+_det_name).style.opacity = 1
  // Enabled close button
  document.getElementById('close_'+_det_id+'-'+_det_attribute+'-'+_det_name).classList.remove("d-none")
  document.getElementById('remove_'+_det_id+'-'+_det_attribute+'-'+_det_name).classList.add("d-none")
  // Enabled edit button, opacity 1
  var divtext_area = document.getElementById("divtext_"+_det_name)
  if (divtext_area) {
    divtext_area.classList.remove("d-none");
  }

  // Enabled updated button (blue color), and opacity 1
  document.getElementById("btn_save_canvas").disabled = false
  // document.getElementById("btn_make_zoom").disabled = false
  document.getElementById('current_page').disabled = false
  document.getElementById('current_page').value = (select_att.value).toString()
  document.getElementById('btn_arrow_left').disabled = false
  document.getElementById('btn_arrow_right').disabled = false
  var val = select_att.value
  var num_pages = document.getElementById('num_pages').val
  if (val <= 1){
    document.getElementById('btn_arrow_left').disabled = true
  }
  if (val >= num_pages){
    document.getElementById('btn_arrow_right').disabled = true
  }
  _page = val
  // {{detail.det_id}}-{{detail.det_attribute}}-{{detail.det_name}}
  document.getElementById('select_page').value = _det_id + "-" + _det_attribute
  document.getElementById('pages_text').value = pages_text
  let _page_pos = pages_list.indexOf((val).toString())
  console.log("Current POS")
  console.log(_page_pos)
  document.getElementById('pages_pos').value = _page_pos

  if (!select_att.value){
    alert("Debe seleccionar la página")
    goPage(1, pdf_id)
  }
  else {
    goPage(select_att.value, pdf_id)
  }
  // loadCanvas()
  // Active values for canvas ...
  var det_x = document.getElementById('det_x-'+_det_name).value
  var det_y = document.getElementById('det_y-'+_det_name).value
  var det_width = document.getElementById('det_width-'+_det_name).value
  var det_height = document.getElementById('det_height-'+_det_name).value
  
  if (det_x != null && det_y != null) {
    ctx.strokeStyle = "red";
    ctx.lineWidth = 4;
    ctx.opacity = 2
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

  // Enabled all controls by name
  var vectors = document.getElementsByName('vectors');
  for (var vector of vectors){
    let vector_id = vector.id
    let get_id = vector_id.split("_")
    document.getElementById("vector_"+get_id[1]).disabled = false;
    document.getElementById("remove_"+get_id[1]).disabled = false;
    document.getElementById("remove_"+get_id[1]).style.opacity = 1
  }

  // Disabled vector button
  document.getElementById('vector_'+_det_id+'-'+_det_attribute+'-'+_det_name).style.opacity = 0.5
  // Disabled close button
  document.getElementById('close_'+_det_id+'-'+_det_attribute+'-'+_det_name).classList.add("d-none")
  document.getElementById('remove_'+_det_id+'-'+_det_attribute+'-'+_det_name).classList.remove("d-none")
  // Disabled edit button, opacity 1
  var divtext_area = document.getElementById("divtext_"+_det_name)
  if (divtext_area) {
    divtext_area.classList.add("d-none");
  }

  // Disabled updated button (blue color), and opacity 1
  document.getElementById("btn_save_canvas").disabled = true
  // document.getElementById("btn_make_zoom").disabled = true
  document.getElementById('current_page').disabled = true
  document.getElementById('btn_arrow_left').disabled = true
  document.getElementById('btn_arrow_right').disabled = true
  var val = _page
  if (val <= 1){
    document.getElementById('btn_arrow_left').disabled = true
  }
  if (val >= pages.value){
    document.getElementById('btn_arrow_right').disabled = true
  }

  // clear the canvas
  //   ctx.clearRect(0, 0, canvas.width, canvas.height);
  isDown = false
}

// ADD ATTRIBUTE
function addAttribute() {
  // Disabled add attribute
  document.getElementById('add_attribute').classList.add("d-none")
  // Enabled div attribute
  document.getElementById('div_attribute').classList.remove("d-none")
}

// CANCEL ATTRIBUTE
function cancelAttribute(edit_id) {
  // Disbled div attribute
  document.getElementById('div_attribute').classList.add("d-none")
  document.getElementById('new_attribute').value = ""
  // Enabled add attribute
  document.getElementById('add_attribute').classList.remove("d-none")
}

// REMOVE ATTRIBUTE
function delAttribute(url, pro_id, att_name, edit_id) {

  if (confirm('Desea eliminar el atributo ' + att_name)) {
    // Save it!
    // Disabled select option
    let detail_id = edit_id.split("_")
    let detail_edit = detail_id[1].split("-")
    _det_id = detail_edit[0]
    // console.log(_det_id)
    
    // Create a new FormData instance
    var data = new FormData();
    // Create a XMLHTTPRequest instance
    var request = new XMLHttpRequest();

    // Set the response type
    request.responseType = "json";

    var action = "remove_attribute";
    data.append("action", action);
    data.append("pro_id", pro_id);
    data.append("det_id", _det_id);

    // request load handler (transfer complete)
    request.addEventListener("load", function (e) {
      if (request.status == 200) {
        /// Disabled updated button (blue color), and opacity 1
        update_att.disabled = true      
        // alert(`Eliminación Exitosa`, "success");
        showAlertPage('Atributo eliminado con éxito', 'success')
        location.reload();
      }
      else {
        // alert(`Alerta en eliminación`, "warning");
        showAlertPage('Atributo no fue eliminado', 'warning')
      }
      if (request.status == 300) {
        // alert(`${request.response.message}`, "warning");
        showAlertPage(`${request.response.message}`, 'warning')
      }
      
    });

    // request error handler
    request.addEventListener("error", function (e) {
      // alert(`Error eliminando el atributo`, "danger");
      showAlertPage('Error eliminando atributo', 'danger')
    });

    // Open and send the request
    request.open("POST", url);
    request.send(data);
  }
  else {
    // Do nothing!
    console.log('Nothing');
  }
}

// SAVE CANVAS
// --------------------------------------------------------------------------------------------------------
function saveCanvas(url, pro_id) {
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

  var action = "save_canvas";
  data.append("action", action);
  data.append("pro_id", pro_id);
  data.append("det_id", _det_id);
  data.append("det_attribute", _det_attribute);
  data.append("page", _page);
  data.append("dictCanvas", JSON.stringify(dictCanvas));

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      // Disabled updated button (blue color), and opacity 1
      update_att.disabled = true
      // alert(`Registro Exitoso`, "success");
      showAlertPage('Canvas actualizado con éxito', 'success')
      location.reload();
    }
    else {
      showAlertPage('Canvas no fue actualizado', 'warning')
    }
    if (request.status == 300) {
      showAlertPage(`${request.response.message}`, 'warning')
    }
    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    // alert(`Error procesando la imagen`, "danger");
    showAlertPage('Error actualizando canvas', 'danger')
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);
}

// MAKE ZOOM
// --------------------------------------------------------------------------------------------------------
function makeZoom(url, pro_id) {
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

  var action = "make_zoom";
  data.append("action", action);
  data.append("pro_id", pro_id);
  data.append("det_id", _det_id);
  data.append("det_attribute", _det_attribute);
  data.append("page", _page);
  data.append("dictCanvas", JSON.stringify(dictCanvas));

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      // Disabled updated button (blue color), and opacity 1
      update_att.disabled = true
      console.log("path_page")
      console.log(request.response.path_page)

      canvas_pdf = document.getElementById("canvasContainer")
      canvas_pdf.innerHTML = `
      <canvas id="canvas" style="background-image: url('${request.response.path_page}'); position: relative; opacity: 0.85; margin: 0 auto;" width="640px" height="820px"></canvas>
      `
      showAlertPage('Zoom actualizado con éxito', 'success')
    }
    else {
      showAlertPage('Zoom no fue actualizado', 'warning')
    }
    if (request.status == 300) {
      showAlertPage(`${request.response.message}`, 'warning')
    }
    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    // alert(`Error procesando la imagen`, "danger");
    showAlertPage('Error generando zoom', 'danger')
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);
}

// --------------------------------------------------------------------------------------------------------
function saveText(url, pro_id, det_name) {
  console.log("saveText")
  let text = "text_" + det_name
  var text_area = document.getElementById(text)
  console.log(text_area.value)
  console.log(_page)
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
  data.append("pro_id", pro_id);
  data.append("det_id", _det_id);
  data.append("det_attribute", _det_attribute);
  data.append("det_value", text_area.value);
  data.append("page", _page);

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      /// Disabled updated button (blue color), and opacity 1
      update_att.disabled = true
      
      showAlertPage('Texto actualizado con éxito', 'success')
      location.reload();
    }
    else {
      // alert(`Alerta en registro`, "warning");
      showAlertPage('Texto no fue actualizado', 'warning')
    }
    if (request.status == 300) {
      // alert(`${request.response.message}`, "warning");
      showAlertPage(`${request.response.message}`, 'warning')
    }
    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    showAlertPage('Error actualizando texto', 'danger')
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);
}

// --------------------------------------------------------------------------------------------------------
function saveAttribute(url, pro_id) {
  console.log("saveAttribute")
  // let text = "text_" + det_name
  var new_att = document.getElementById('new_attribute')
  var det_type = document.getElementById('det_type')
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
  data.append("pro_id", pro_id);
  data.append("new_att", new_att.value);
  data.append("det_type", det_type.value);

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      /// Disabled updated button (blue color), and opacity 1
      update_att.disabled = true
      showAlertPage('Atributo registrado con éxito', 'success')
      location.reload();
    }
    else {
      showAlertPage('Atributo no fue registrado', 'warning')
    }
    if (request.status == 300) {
      showAlertPage(`${request.response.message}`, 'warning')
    }
    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    showAlertPage('Error registrando atributo', 'danger')
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);
}

// Reload Page
function loadPage() {
  location.reload();
}

var text_title = document.getElementById("text_título");
var text_autor = document.getElementById("text_autor");
var text_anio = document.getElementById("text_año");

if (text_title.innerHTML == '' || text_autor.innerHTML == '' || text_anio.innerHTML == '') {
  document.getElementById("save_pdf").disabled = true
  var msg_down = "Debe registrar "

  if (text_title.innerHTML == '') {
    msg_down = msg_down + ", Título"
  }
  if (text_autor.innerHTML == '') {
    msg_down = msg_down + ", Autor"
  }
  if (text_anio.innerHTML == '') {
    msg_down = msg_down + ", Año"
  }
  
  msg_down = document.getElementById("msg_download").innerHTML = msg_down
}
else{
  document.getElementById("save_pdf").disabled = false
}