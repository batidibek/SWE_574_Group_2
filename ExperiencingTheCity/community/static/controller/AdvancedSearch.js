function searchPost() {
    document.getElementById("filteredposts").innerHTML = "";
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
    filtered_posts = postList.filter(function (post) {
            console.log(post);
            var postFields = JSON.parse(post.form_fields);
            console.log(postFields);
            for (var sField in postFields) {
                if (postFields.hasOwnProperty(sField)) {

                    var scname = postFields[sField].fieldlabel + "_sc";
                    searchCriteria = document.getElementById("searchForm").elements.namedItem(scname).value;
                    var inputname1 = postFields[sField].fieldlabel + "_1";
                    var value1 = document.getElementById("searchForm").elements.namedItem(inputname1).value;
                    var inputname2 = postFields[sField].fieldlabel + "_2";
                    var value2 = document.getElementById("searchForm").elements.namedItem(inputname2).value;


                    switch (searchCriteria) {
                        case "EQ":
                            if (value1 !== "") {
                                return postFields[sField].fieldValue.toLowerCase() === value1.toLowerCase();
                            }

                            break;
                        case "CS":
                            if (value1 !== "") {
                                return postFields[sField].fieldValue.toLowerCase().includes(value2.toLowerCase());
                            }
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


        }
    );

    console.log(filtered_posts);
    // document.getElementById("filteredposts").innerHTML = JSON.stringify(filtered_posts);
    document.getElementById("filtered_posts").value = JSON.stringify(filtered_posts)

    addPostTiles(filtered_posts);

}

function addPostTiles(postList) {
    for (var i = 0; i < postList.length; i++) {
        var colDiv = document.createElement("div");
        colDiv.setAttribute("class", "col-md-4");


        var cardDiv = document.createElement("div");
        cardDiv.setAttribute("class", "row no-gutters border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative");

        var bodyDiv = document.createElement("div");
        bodyDiv.setAttribute("class", "col p-4 d-flex flex-column position-static");

        var postH1 = document.createElement("h3");
        postH1.setAttribute("class", "mb-0");
        var header = document.createTextNode(postList[i].name);
        postH1.appendChild(header);

        var postDate = document.createElement("div");
        postDate.setAttribute("class", "mb-1 text-muted");
        var date = document.createTextNode(postList[i].creation_date);
        postDate.appendChild(date);

        var postDesc = document.createElement("p");
        postDesc.setAttribute("class", "card-text mb-auto");
        var desc = document.createTextNode(postList[i].description.substring(0, 15));
        postDesc.appendChild(desc);

        var btnGrp = document.createElement("div");
        btnGrp.setAttribute("class", "btn-group");
        var btn = document.createElement("button");
        btn.setAttribute("type", "button");
        btn.setAttribute("style", "margin: 2px;");
        btn.setAttribute("class", "btn btn-sm btn-outline-secondary");

        var a = document.createElement("a");
        var href = "/communities/posts/post_detail/" + postList[i].id
        a.setAttribute("href", href);
        var atext = document.createTextNode("View Detail");
        a.appendChild(atext);

        btn.appendChild(a);
        btnGrp.appendChild(btn);


        bodyDiv.appendChild(postH1);
        bodyDiv.appendChild(postDate);
        bodyDiv.appendChild(postDesc);
        bodyDiv.appendChild(btnGrp);
        cardDiv.appendChild(bodyDiv);
        colDiv.appendChild(cardDiv);
        document.getElementById("filteredposts").appendChild(colDiv);


    }

}