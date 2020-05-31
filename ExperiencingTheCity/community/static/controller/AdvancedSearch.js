function searchPost() {
    var postTypeId = document.getElementById("postTypeId").value;

    console.dir(postTypeId);


    jQuery.ajax({
        type: "GET", url: "/getPostsOfPostType",
        data: {"pt_id": postTypeId},
        async: false,
        success:
            function (result) {
                console.log(result);
                var postList = result.posts;
                filterPosts(postList);

            },
        error:
            function (returnVal) {
                console.log(returnVal);
                if (returnVal.status === 404) {

                }

            }
    });
}

function filterPosts(postList) {
    var searchCriteria = "";
    var filtered_posts = postList.filter(function (post) {
        console.log(post);
        var postFields = JSON.parse(post.form_fields);
        console.log(postFields);
        for (sField in postFields) {

            var scname = postFields[sField].fieldlabel + "_sc";
            searchCriteria = document.getElementById("searchForm").elements.namedItem(scname).value;
            var inputname1 = postFields[sField].fieldlabel + "_1";
            var value1 = document.getElementById("searchForm").elements.namedItem(inputname1).value;
            var inputname2 = postFields[sField].fieldlabel + "_2";
            var value2 = document.getElementById("searchForm").elements.namedItem(inputname2).value;


            switch (searchCriteria) {
                case "EQ":
                    return postFields[sField].fieldValue.toLowerCase() === value1.toLowerCase();
                    break;
                case "CS":
                    return postFields[sField].fieldValue.toLowerCase().includes(value2.toLowerCase());
                    break;
                case "GT":
                    break;
                case "GE":
                    break;
                case "LT":
                    break;
                case "LE":
                    break;
                case "BT":
                    break;
            }


        }


        searchCriteria = document.getElementById("searchForm").elements.namedItem("name_sc").value;
        var name1 = document.getElementById("searchForm").elements.namedItem("name1").value;
        var name2 = document.getElementById("searchForm").elements.namedItem("name2").value;
        switch (searchCriteria) {
            case "EQ":
                return post.name.toLowerCase() === name1.toLowerCase();
                break;
            case "CS":
                return post.name.toLowerCase().includes(name1.toLowerCase());
                break;
            case "GT":
                break;
            case "GE":
                break;
            case "LT":
                break;
            case "LE":
                break;
            case "BT":
                break;
        }

        searchCriteria = document.getElementById("searchForm").elements.namedItem("desc_sc").value;
        var desc1 = document.getElementById("searchForm").elements.namedItem("description1").value;
        var desc1 = document.getElementById("searchForm").elements.namedItem("description2").value;

        switch (searchCriteria) {
            case "EQ":
                return post.description.toLowerCase() === name1.toLowerCase();
                break;
            case "CS":
                return post.description.toLowerCase().includes(name1.toLowerCase());
                break;
            case "GT":
                break;
            case "GE":
                break;
            case "LT":
                break;
            case "LE":
                break;
            case "BT":
                break;
        }


    });

     console.log(filtered_posts);

}