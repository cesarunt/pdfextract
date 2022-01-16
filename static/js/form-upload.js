// Define variables

// var search_terms = ['apple', 'apple watch', 'apple macbook', 'apple macbook pro', 'iphone', 'iphone 12'];
var variables = document.getElementById("keywords").value;
variables = variables.replace(']', '').replace('[', '')
variables = variables.split(', ')
var search_terms = []

for (var i = 0; i < variables.length; i++) {
    search_terms.push(variables[i].replace(']', '').replace('[', ''))
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
  let terms = autocompleteMatch(val);
  for (i=0; i<terms.length; i++) {
    list += '<li>' + terms[i] + '</li>';
  }
  res.innerHTML = '<ul>' + list + '</ul>';
}