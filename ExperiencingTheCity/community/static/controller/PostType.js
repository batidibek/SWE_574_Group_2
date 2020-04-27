$(document).ready(function () {


    $(window).keydown(function (event) {
        if (event.keyCode == 13) {

            if ( $(event.target).attr("name") == "enum_vals") {
                event.preventDefault();
            }

        }
    });

    var counter = 0;

    if (isEdit === true) {
        addDataTypeFields(document.getElementById("PostTypeFields").value);
    }

    $("#addDataField").on("click", function () {

        counter++
        var row = document.getElementById("rowToClone_0"); // find row to copy
        var table = document.getElementById("tableToModify"); // find table to append to
        var clone = row.cloneNode(true); // copy children too
        clone.id = "rowToClone_" + counter.toString(); // change id or other attributes/contents
        clone.cells[5].innerHTML = "<button type='button' class='btn removeDataField' onclick='removePostField(this);'><span class='fa fa-minus'> </span></button>";
        clone.cells[3].innerHTML = '<input type="text" class="enum_vals form-control "\n' +
            '                                   name="enum_vals" data-role="tagsinput" disabled>';
        table.appendChild(clone); // add new row to end of table
    });

    $("#createPostType").on("click", function (event) {

       var enumValuesOfRows = $('input[name=enum_vals]').tagsinput("items");

        var tagsJson = '{ "enums" : [] }';
        var table = document.getElementById("myTable");
        var obj = JSON.parse(fieldJson);
        for (var i = 1, row; row = table.rows[i]; i++) {
            //iterate through rows
            //rows would be accessed using the "row" variable assigned in the for loop

            var fieldTypes = row.cells[2].children[0];
            var fieldTypesSel = fieldTypes.options[fieldTypes.selectedIndex].text;
            if (fieldTypes.options[fieldTypes.selectedIndex].value === "EN") {
                var enumValList = enumValuesOfRows[i - 1];
                for (var j = 0; j < enumValList.length; j++) {
                    var obj2 = JSON.parse(tagsJson);
                    obj2['enums'].push({
                        "enum": enumValList[j]
                    });
                    tagsJson = JSON.stringify(obj2);
                }
            }

            var isRequired = row.cells[4].children[0].children[0];
            obj['theFields'].push({
                "fieldposnr": row.cells[0].children[0].value,
                "fieldlabel": row.cells[1].children[0].value,
                "fieldtype": fieldTypes.options[fieldTypes.selectedIndex].value,
                "isRequired": isRequired.checked,
                "enumvals": fieldTypes.options[fieldTypes.selectedIndex].value === "EN" ? tagsJson : ""
            });

        }
        fieldJson = JSON.stringify(obj);
        console.log(fieldJson);
        $("#postTypeFields").val(fieldJson);
    });

});

function removePostField(oEvent) {
    $(oEvent).closest("tr").remove();
}


function addDataTypeFields(oFormFields) {

    if (oFormFields !== "") {
        var flds = JSON.parse(oFormFields);

        console.log(flds['theFields']);

        var fieldList = flds['theFields'];


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
        $this.parent('td').parent('tr').find("input[name='enum_vals']").prop("disabled", false);
    } else {
        $this.parent('td').parent('tr').find("input[name='enum_vals']").prop("disabled", true);
    }
}


