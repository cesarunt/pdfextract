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

  const var_list = []
  
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
    // if (list != ''){
    //   list += '<li class="line" style="margin: 1px auto;"></li>'
    //   list += '<li id="0" data_id="0" data_value="Agregar">Agregar ...</li>';
    // }

    res.innerHTML = '<ul id="keywords_found">' + list + '</ul>';

    var listul = document.getElementById ("keywords_found");
    var liTags = listul.getElementsByTagName ("li");

    for (var i = 0; i < liTags.length; i++) {
      // liTags[i].value = i + 3;
      var variable = "key_" + i.toString()
      document.getElementById(variable).onclick = function(event) {
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

// FUNCTIONS FOR 