// Canvas 
// Dictionary for Canvas Multiple
var dictCanvas = [];

// --------------------------------------------------------------------------------------------------------------
var _x = null
var _y = null
var _w = null
var _h = null
var _page = 1
var select_index = 0
var select_control = ""


function setValueItem(_this, _index) {
    select_index = _index
    select_control = _this.id
}

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
        // console.log("DICT")
        // console.log(objects)
        // console.log(dictCanvas)
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


$("canvas").dblclick(function() {
  cleanCanvas();
  // ctx.clearRect(0, 0, canvas.width, canvas.height);
//   var objects = canvas.getObjects();
//   for(var i = 0; i < objects.length; i++){   
//     canvas.remove(objects[i]);
//   };
//   canvas.clear();
//   dictCanvas = []
});

function cleanCanvas(canvas) {
    // console.log("clear ....")
    if (canvas != null){
        var objects = canvas.getObjects();
        for(var i = 0; i < objects.length; i++){   
            canvas.remove(objects[i]);
        };
        canvas.clear();
        dictCanvas = []
    }
}

// Get a reference to the alert wrapper
var alert_wrapper = document.getElementById("alert_wrapper");


// GET CANVAS
// --------------------------------------------------------------------------------------------------
function getTextCanvas(url, index, path) {
  // Reject if the file input is empty & throw alert
  if (!_x && !_y) {
    alert("Debe seleccionar texto del voucher", "warning")
    return;
  }

  // Create a new FormData instance
  var data = new FormData();
  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();
  // Set the response type
  request.responseType = "json";

  var text_canvas = ""
  var action = "get_canvas";
  data.append("action", action);
  data.append("index", index);
  data.append("path", path);
  data.append("dictCanvas", JSON.stringify(dictCanvas));

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
        text_canvas = request.response['text_canvas']
        if (select_control == "") {
            alert(`Debe seleccionar un imtem`, "success");
        }
        else {
            div_modal = document.getElementById("exampleModal_"+select_index)
            div_item = div_modal.querySelector("#div_items").querySelector(('#'+select_control).toString())
            div_item.value = text_canvas
        }
    }
    else {
        console.log('Canvas no fue actualizado')
    }    
  });

  // request error handler
  request.addEventListener("error", function (e) {
    alert(`Error procesando la imagen`, "danger");
    // showAlertPage('Error actualizando canvas', 'danger')
  });

  // Open and send the request
  request.open("POST", url);
  request.send(data);
}

// Reload Page
function loadPage() {
  location.reload();
}