// Define variables

var variables = document.getElementById("keywords");
// var keyword1 = document.getElementById("keyword1");
// var keyword2 = document.getElementById("keyword2");
// var keyword3 = document.getElementById("keyword3");

const var_list = []

if (variables){
    var count = document.getElementById("n_keywords").value;
    for(let i=1; i<=count; i++){
        var variable = "key_" + i.toString()
        document.getElementById(variable).onclick = function(event) {
            // console.log(var_list.indexOf(this.id))
            if (var_list.indexOf(this.id) >= 0) {
                this.classList.remove("btn-primary");
                this.classList.add("btn-secondary");
                var_list.pop(this.id)
            } 
            else {
                if (var_list.length < 3) {
                    this.classList.remove("btn-secondary");
                    this.classList.add("btn-primary");
                    var_list.push(this.id)
                    // console.log(var_list)
                }
                else {
                    alert("Seleccionar 3 variables. O deseleccionar las variables anteriores.")
                }
            }
            console.log(var_list)
        }
    }
}


// Function to validate Submit form_upload
function validateFormUpload(url) {
    if (var_list.length > 0) {
        for(let i=1; i<=var_list.length; i++){
            var keyword = "keyword_" + i.toString()
            document.getElementById(keyword).value = var_list[i-1];
        }
    }
}