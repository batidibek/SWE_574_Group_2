$(document).ready(function () {

    $("#createpost").keydown(function (event) {
        if (event.keyCode == 13) {
            event.preventDefault();
        }
    });

    if (isEdit === true) {
        addDataTypeFields(document.getElementById("PostTypeFields").value);
    }

    $("#addDataField").on("click", function () {
        var new_row = $("#PostTypeFieldsTable tr:last").clone().find('input').val('').end();
        new_row.find('#addDataBtn').removeClass('fa fa-plus');
        new_row.find('#addDataBtn').addClass('fa fa-minus').attr('onclick', 'removePostField(this)');
        new_row.find('.bootstrap-tagsinput').remove();
        new_row.find('#enumValues1').tagsinput();

        $("#PostTypeFieldsTable").append(new_row);
    });

    $("#createPostType").on("click", function (event) {
         var json = html2json();
         $("#postTypeFields").val(json);
    });
});

function removePostField(oEvent) {
    $(oEvent).closest("tr").remove();
}


function addDataTypeFields(oFormFields) {

    if (oFormFields !== "") {
        var flds = JSON.parse(oFormFields);

        var fieldList = flds['fields'];

        var lv_fieldtype = "";
        var obj = JSON.parse(fieldJson);

        var row = document.getElementById("rowToClone_0"); // find row to copy
        var table = document.getElementById("tableToModify"); // find table to append to
        var clone = row.cloneNode(true); // copy children too
        for (var i = 0; i < fieldList.length; i++) {
            var enumString = "";

            clone.id = "rowToClone_" + i.toString(); // change id or other attributes/contents

            clone.cells[5].innerHTML = "<button type='button' class='btn removeDataField' onclick='removePostField(this);'><span class='fa fa-minus'> </span></button>";
            clone.cells[0].getElementsByTagName("input")[0].value = fieldList[i].fieldposnr;
            clone.cells[1].getElementsByTagName("input")[0].value = fieldList[i].fieldlabel;
            clone.cells[2].getElementsByTagName("select")[0].value = fieldList[i].fieldtype;
            if (fieldList[i].fieldtype === "EN") {
                var enums = JSON.parse(fieldList[i].enumvals);
                var enumList = enums["enums"];

                for (var j = 0; j < enumList.length; j++) {
                    if (j == enumList.length - 1) {
                        enumString += enumList[j].enum
                    } else {
                        enumString += enumList[j].enum + ", ";
                    }
                }
                clone.cells[3].getElementsByTagName("input")[0].value = enumString;
            }
            table.appendChild(clone); // add new row to end of table
        }
    }


}

function onSelectFType(oEvent) {
    var $this = $(oEvent);

    if ($(oEvent).val() == "EN") {
        $this.parent('td').parent('tr').find("input[name='enum_vals']").prop("disabled", false).prop("enabled", false);
    } else {
        $this.parent('td').parent('tr').find("input[name='enum_vals']").prop("disabled", true).prop("enabled", true);
    }
}


function html2json() {
    var enumValuesOfRows = $('input[name=enum_vals]').tagsinput("items");
    var tagsJson = ' { "enumvals" : [] } ';
    var table = document.getElementById("PostTypeFieldsTable");

    var json = '{ "fields": {';
    var otArr = [];
  
    for (var i = 1, row; row = table.rows[i]; i++) {

        var itArr = [];

        var fieldTypes = row.cells[2].children[0];
        // var fieldTypesSel = fieldTypes.options[fieldTypes.selectedIndex].text;
        if (fieldTypes.options[fieldTypes.selectedIndex].value === "EN") {
            // var enumValList = enumValuesOfRows.itemsArray;
            var enumValList = enumValuesOfRows.itemsArray;
             var obj2 = [];
            for (var j = 0; j < enumValList.length; j++) {
                //var obj2 = JSON.parse(tagsJson);

                obj2.push({
                    enum: enumValList[j]
                });

            }
             tagsJson = JSON.stringify(obj2);
        }

        var isRequired = row.cells[4].children[0].children[0];

        var first_cell  = '"fieldposnr" : "' + row.cells[0].children[0].value + '"';
        var second_cell = '"fieldlabel" : "' + row.cells[1].children[0].value + '"';
        var third_cell  = '"fieldtype"  : "' + fieldTypes.options[fieldTypes.selectedIndex].value + '"';
        var forth_cell  = '"isRequired" : "' + isRequired.checked + '"';
        var fifth_cell  = '"enumvals" : ' + (fieldTypes.options[fieldTypes.selectedIndex].value === "EN" ? tagsJson : '') ;


        itArr.push(first_cell);
        itArr.push(second_cell);
        itArr.push(third_cell);
        itArr.push(forth_cell);
        itArr.push(fifth_cell);
    
        otArr.push('"' + (i) + '": {' + itArr.join(",") + '}');
    }

    json += otArr.join(",") + '}}';
 
    return json;
 }