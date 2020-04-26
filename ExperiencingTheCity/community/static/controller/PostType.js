$(document).ready(function () {
    var counter = 0;

    $("#addDataField").on("click", function () {

        counter++
        var row = document.getElementById("rowToClone_0"); // find row to copy
        var table = document.getElementById("tableToModify"); // find table to append to
        var clone = row.cloneNode(true); // copy children too
        clone.id = "rowToClone_" + counter.toString(); // change id or other attributes/contents
        clone.cells[5].innerHTML =  "<button type='button' class='btn removeDataField' onclick='removePostField();'><span class='fa fa-minus'> </span></button>";
        table.appendChild(clone); // add new row to end of table
    });

    $("#createPostType").on("click", function () {
        var tagsJson = '{ "enums" : [] }';
        var table = document.getElementById("myTable");
        var obj = JSON.parse(fieldJson);
        for (var i = 1, row; row = table.rows[i]; i++) {
            //iterate through rows
            //rows would be accessed using the "row" variable assigned in the for loop
            var fieldTypes = row.cells[2].children[0];
            var fieldTypesSel = fieldTypes.options[fieldTypes.selectedIndex].text;

            var isRequired = row.cells[4].children[0];
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
        //
        // var csrftoken = getCookie('csrftoken');
        //
        // $.ajaxSetup({
        //     beforeSend: function (xhr, settings) {
        //         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        //             xhr.setRequestHeader("X-CSRFToken", csrftoken);
        //         }
        //     }
        // });
        //
        // jQuery.ajax({
        //     type: "POST", url: "/newPostType",
        //     data: {"communityId": document.getElementById("communityId").value,
        //            "postTypeFields": fieldJson},
        //     success:
        //         function (result) {
        //             $('#confirmDeactivation').modal('hide');
        //             window.location.href = "/";
        //         }
        // });

    });
});
