function searchCommunity() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value;
    var dataList = $("#foundCommunities");
    if (filter === "") {
        dataList.empty();
        return;
    }
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