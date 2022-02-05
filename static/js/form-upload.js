// Define keywords

// FUNCTIONS FOR AUTOCOMPLETE KEYWORDS
var variables_select = document.getElementById("keywords_select");
var variables_label = document.getElementById("keywords_label");
var keywords = document.getElementById("keywords_in").value;
var keywords_out = document.getElementById("keywords_out");
// console.log(keywords)
keywords = keywords.replace(']', '').replace('[', '')
keywords = keywords.split(', ')
var search_terms = []
var var_list = []
var terms = []

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

  var var_list = []
  
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
      // liTags[i].value = i + 3;
      var variable = "key_" + i.toString()
      document.getElementById(variable).onclick = function(event) {
        variables_label.classList.remove("d-none");
        let current_id = $(this).attr('data_id')
        if (var_list.indexOf(current_id) < 0){
          var_list.push(current_id)
          variables_label.classList.remove("d-none");
          variables_select.innerHTML += '<button id="'+current_id+'" type="button" value="'+current_id+'" class="btn btn-secondary mb-2" style="padding: 0.25rem 0.5rem;">'+$(this).attr('data_value')+'</button>&nbsp;'
          keywords_out.value = var_list
          console.log(keywords_out.value)
        }
      }
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

// ADD VARIABLE FUNCTION
// --------------------------------------------------------------------------------------------------------
function addVariable() {
  var value = document.getElementById("keyword").value;

  // Reject if the file input is empty & throw alert
  if (!value) {
    alert("Ingresar texto de la variable", "warning")
    return;
  }
  if (!value.match("^[A-Za-z]{1,30}")) {
    alert("Ingrese caracteres de texto", "warning")
    return;
  }
  if (value.length < 4) {
    alert("Ingresar texto de la variable", "warning")
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
      
      alert(`Registro Exitoso`, "success");
      location.reload();
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