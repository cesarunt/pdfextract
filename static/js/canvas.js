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
function activeAttribute(edit_id, pdf_id) {
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
  
  // console.log(det_x)
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

  // clear the canvas
  //   ctx.clearRect(0, 0, canvas.width, canvas.height);
  isDown = false
}

// ADD ATTRIBUTE
function addAttribute(edit_id) {
  // Disabled add attribute
  document.getElementById('add_attribute').classList.add("d-none")
  // Abled div attribute
  document.getElementById('div_attribute').classList.remove("d-none")
}

// CANCEL ATTRIBUTE
function cancelAttribute(edit_id) {
  // Disbled div attribute
  document.getElementById('div_attribute').classList.add("d-none")
  document.getElementById('new_attribute').value = ""
  // Abled add attribute
  document.getElementById('add_attribute').classList.remove("d-none")
}

// REMOVE ATTRIBUTE
function delAttribute(url, edit_id) {
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

// --------------------------------------------------------------------------------------------------------
function saveCanvas(url) {
  console.log("saveCanvas")

  // Reject if the file input is empty & throw alert
  if (!_x && !_y) {
    alert("Debe seleccionar texto de la imagen", "warning")
    return;
  }
  // console.log(_x)
  // console.log(_y)
  // console.log(_w)
  // console.log(_h)
  // console.log(_det_id)
  // console.log(_det_attribute)

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
  // data.append("x", _x);
  // data.append("y", _y);
  // data.append("w", _w);
  // data.append("h", _h);
  data.append("page", _page);
  data.append("dictCanvas", JSON.stringify(dictCanvas));

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      /// Disabled updated button (blue color), and opacity 1
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