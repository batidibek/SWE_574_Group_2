function searchCommunity(event) {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value;
    var dataList = $("#foundCommunities");
    if (filter === "") {
        dataList.empty();
        return;
    }

    var selectedCommunity = $("#foundCommunities option[value='" + $('#searchInput').val() + "']").attr('text');
    if (selectedCommunity !== undefined) {
        var location = "communities/" + selectedCommunity;
        window.location.href = location;
    } else {

        jQuery.ajax({
            type: "GET", url: "/getCommunityByFilter",
            data: {"filterString": filter},
            async: false,
            success:
                function (result) {

                    dataList.empty();
                    console.log(result.communities);
                    if (result.communities) {
                        for (var i = 0; i < result.communities.length; i++) {
                            var opt = $("<option></option>").attr("value", result.communities[i].name);
                            opt.attr("text", result.communities[i].id);
                            dataList.append(opt);
                        }
                    }

                },
            error:
                function (returnVal) {
                    dataList.empty();
                    console.log(returnVal);
                    if (returnVal.status === 404) {

                    }

                }
        });
    }
}

$(document).on('keypress', function (e) {

    if (e.which == 13) {

        var dataList = $("#foundCommunities");

        var comList = dataList[0].options;
        var idList = [];
        for (var i = 0; i < comList.length; i++) {
            idList.push(Number(comList[i].getAttribute("text")));
        }

        console.log(idList);

        var url = $("#Url").attr("data-url");
        jQuery.ajax({
            type: "GET",
            // url: "/getCommunityListByFilter",
            url: url,
            data: {"idList[]": idList},
            async: false,
            dataType: "json",
            contentType: "application/x-www-form-urlencoded/json",
            success:
                function (result) {
                    dataList.empty();
                    $('#cmnList').html(result);
                },
            error:
                function (returnVal) {
                    dataList.empty();
                    console.log(returnVal);
                    if (returnVal.status === 404) {

                    }

                }
        });

    }
});


