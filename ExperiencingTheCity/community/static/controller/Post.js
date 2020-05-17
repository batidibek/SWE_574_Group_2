$(document).ready(function(){
    $('input[type="file"]').change(function(e){
        var idVal = $(this).attr('id');
        var geekss = e.target.files[0].name;

        labels = document.getElementsByTagName('label');
        for( var i = 0; i < labels.length; i++ ) {
            if (labels[i].htmlFor == idVal)
                labels[i].innerHTML = geekss;
        }
    });
});


$(function() {
      $("#search").on("click", function() {
          var searchTerm = $("#searchTerm").val();
          
          console.log(searchTerm);

          if(searchTerm == null){
            document.getElementById("searchTerm").value = "Johnny Bravo";
          }

          var url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&limit=500&language=en&format=json&search="+ searchTerm +"&origin=*";
          $.ajax({
              url: url,
              type: 'GET',
              contentType: "application/json; charset=utf-8",
              async: false,
              dataType: "json",
              success: function(data, status, jqXHR) {

                for(var i = 0; i < data['search'].length; i++){
                    result = data['search'][i];
                    input_value = '{ "id":"' + result.id + '", "label":"' + result.label + '", "description":"' + result.description + '"}';

                    var div_node = document.createElement("DIV");
                    div_node.setAttribute("class", "form-check");

                    var input_node = document.createElement("INPUT");
                    input_node.setAttribute("type", "checkbox");
                    input_node.setAttribute("name", "wiki_tag");
                    input_node.setAttribute("value", input_value);

                    var label_node = document.createElement("LABEL");
                    label_node.innerHTML = result.id + ' ' + result.label + ': ' + result.description;

                    div_node.appendChild(input_node);
                    div_node.appendChild(label_node);

                    document.getElementById("wikidataResult").appendChild(div_node);
                  }
              }
          })
          .done(function() {
              console.log("success");
          })
          .fail(function() {
              console.log("error");
          })
          .always(function() {
              console.log("complete");
          });
      });
  });