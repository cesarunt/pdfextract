// FUNCTIONS FOR AUTOCOMPLETE KEYWORDS
var variables_select = document.getElementById("keywords_select");
var variables_label = document.getElementById("keywords_label");
var keywords_out = document.getElementById("keywords_out");
var keywords_in = document.getElementById("keywords_in");
var keywords = document.getElementById("keywords");
// var attributes = document.getElementById("attributes");
var departments = document.getElementById("department");
var provinces = document.getElementById("province");
var districts = document.getElementById("district");

if (keywords_in){
  keywords = keywords_in.value;
  keywords = keywords.replace(']', '').replace('[', '')
  keywords = keywords.split(', ')
}

var search_terms = []
var var_list = []
var terms = []
var current_id = 0

if (keywords_out){
  keys = keywords_out.value
  keys = keys.replace(']', '').replace('[', '')
  if (keys!=""){
    var_list = keys.split(', ')
  }
}

if (keywords){
  for (var i = 0; i < keywords.length; i++) {
    search_terms.push(keywords[i].replace("'", "").replace("'", ""))
  }

  function autocompleteMatch(input) {
    if (input == '') {
      return [];
    }
    var reg = new RegExp(input)
    return search_terms.filter(function(term) {
      if (term.match(reg)) {
        return term;
      }
    });
  }
  
  function showResults(val) {
    res = document.getElementById("result");
    res.innerHTML = '';
    let list = '';

    terms = autocompleteMatch(val);
    for (i=0; i<terms.length; i++) {
      var variable = "key_" + i.toString()
      let data_item = terms[i].split('-')
      if (i < 5){
        list += '<li id="'+variable+'" data_id="'+data_item[0]+'" data_value="'+data_item[1]+'">' + data_item[1] + '</li>';
      }
    }
    res.innerHTML = '<ul id="keywords_found">' + list + '</ul>';
    var listul = document.getElementById ("keywords_found");
    var liTags = listul.getElementsByTagName ("li");

    for (var i = 0; i < liTags.length; i++) {
      var variable = "key_" + i.toString()
      selectKeyword(variable);
    }
  }
}

// CANCEL ATTRIBUTE FUNCTION
function clearKeywords() {
  var_list = []
  variables_label.classList.add("d-none");
  variables_select.innerHTML = ""
  keywords_out.value = var_list
}

function selectKeyword(variable){
  // Event onClick, when click on keywords found
  document.getElementById(variable).onclick = function(event) {
    variables_label.classList.remove("d-none");
    current_id = $(this).attr('data_id')
    if (var_list.indexOf(current_id) < 0){
      var_list.push(current_id)
      variables_label.classList.remove("d-none");
      variables_select.innerHTML += '<button id="'+current_id+'" type="button" value="'+current_id+'" class="btn btn-secondary mb-2" style="padding: 0.25rem 0.5rem;">'+$(this).attr('data_value')+'</button>&nbsp;'
      keywords_out.value = var_list
    }
  }
}

var keyword = document.getElementById("keyword");
if (keyword) {
  keyword.addEventListener("keypress", function(event) {
    current_id = document.getElementById("key_id").value;
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      event.preventDefault();
      addVariable(keyword.value, "new");
    }
  });
}

// ACTIVE FILTER FOR BACKGROUNDS AND FRAMEWORKS
function activeBack(_this) {
  document.getElementById("filter_frame").classList.add("d-none");
  document.getElementById("filter_back").classList.remove("d-none");
}

function activeFrame(_this) {
  document.getElementById("filter_back").classList.add("d-none");
  document.getElementById("filter_frame").classList.remove("d-none");
}


function activeGuardar() {
  var checkboxes = document.getElementsByName('pdfs');
  var check_val = false

  for (var checkbox of checkboxes) {
    check = checkbox.checked;
    if (check==true){
      check_val = true
    }
  }
  if (check_val==false){ // Disactivate button and show msg
    document.getElementById("btn_down_canvas").disabled = true
    document.getElementById("btn_save_canvas").disabled = true
    document.getElementById("text_save").classList.remove("d-none");
  }
  else{                  // Activate buttons and hide msg
    document.getElementById("btn_down_canvas").disabled = false
    document.getElementById("btn_save_canvas").disabled = false
    document.getElementById("text_save").classList.add("d-none");
  }
}

// SHOW ATTRIBUTES
function showAttributes(pro_id, pdf_id) {
  fetch('/get_attributes/' + pro_id + '/' + pdf_id).then(function(response){
    response.json().then(function(data){
      let optionHTML_Att = "";
      console.log(data.attributes)
      if (data.attributes.length > 0){
        document.getElementById("att_"+pro_id+"_"+pdf_id).classList.remove("d-none");
        var attributes = document.getElementById("attributes_"+pro_id+"_"+ pdf_id);
        for (let attribute of data.attributes){
          console.log(attribute.det_value)
          if (attribute.det_value){
            optionHTML_Att += '<option value="'+ attribute.det_attribute +'">' + attribute.det_name + ': "' +  attribute.det_value + '"</option>';
          }
        }
        attributes.innerHTML = optionHTML_Att;
      }
      else{
        console.log("NO")
        alert("No tienen atributos o se encuentran vacios");
      }
    });
  });
}

function closeAttributes(pro_id, pdf_id) {
  document.getElementById("att_"+pro_id+"_"+pdf_id).classList.add("d-none");
}

// ADD VARIABLE FUNCTION
// --------------------------------------------------------------------------------------------------------
function clearVariables() {
  document.getElementById ("keywords_found").value = ""
  document.getElementById ("keywords_found").innerHTML = ""
  document.getElementById("keyword").value = ""
  document.getElementById("keyword").focus();
}

// function addVariable_click() {
//   var value = document.getElementById("keyword").value;
//   addVariable(value, "click");
// }

function addVariable(value, type){
  // Reject if the file input is empty & throw alert
  if (!value) {
    alert("Debe ingresar una palabra", "warning")
    return;
  }
  if (!value.match("^[A-Za-z]{1,30}")) {
    alert("Ingrese caracteres de texto válidos", "warning")
    return;
  }
  if (value.length < 4) {
    alert("Ingresar palabra, mínimo de 5 caracteres", "warning")
    return;
  }

  // Create a new FormData instance
  var data = new FormData();
  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();

  // Set the response type
  request.responseType = "json";

  var action = "add";
  var title = document.getElementById("title").value
  data.append("action", action);
  data.append("title", title)
  data.append("value", value);

  // request load handler (transfer complete)
  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      console.log("success")
      if (type == "new") {
        fetch('/last_variable').then(function(response){
          response.json().then(function(data){
            console.log(data.key_id)
            current_id = data.key_id
            variables_label.classList.remove("d-none");
            if (var_list.indexOf(current_id) < 0){
              var_list.push(current_id)
              variables_label.classList.remove("d-none");
              variables_select.innerHTML += '<button id="'+current_id+'" type="button" value="'+current_id+'" class="btn btn-secondary mb-2" style="padding: 0.25rem 0.5rem;">'+keyword.value+'</button>&nbsp;'
              keywords_out.value = var_list
            }
          });
        });
      }
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
  request.open("POST", "/add_variable");
  request.send(data);
}

var department = 0
var province = 0

// Action to change and load provinces list from department
if (departments) {
  departments.onchange = function(){
    
    department = departments.value;
    fetch('/province/' + department).then(function(response){
      response.json().then(function(data){
        let optionHTML_Pro = "";
        for (let province of data.provinces){
          optionHTML_Pro += '<option value="'+ province.prv_id +'">' + province.prv_name + '</option>';
        }
        provinces.innerHTML = optionHTML_Pro;
      });
    });

    province = department + "01"
    fetch('/district/' + province + '/province/' + department).then(function(response){
      response.json().then(function(data){
        let optionHTML_Dis = "";
        for (let district of data.districts){
          optionHTML_Dis += '<option value="'+ district.dis_id +'">' + district.dis_name + '</option>';
        }
        districts.innerHTML = optionHTML_Dis;
      });
    });
  }
}

// Action to change and load districts list from province
if (provinces) {
  provinces.onchange = function(){
    
    province = provinces.value;
    fetch('/district/' + province + '/province/' + department).then(function(response){
      response.json().then(function(data){
        let optionHTML_Dis = "";
        for (let district of data.districts){
          optionHTML_Dis += '<option value="'+ district.dis_id +'">' + district.dis_name + '</option>';
        }
        districts.innerHTML = optionHTML_Dis;
      });
    });
  }
}
