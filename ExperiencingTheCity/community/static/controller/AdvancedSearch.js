function searchPost() {
    var postTypeId = document.getElementById("postTypeId").value;
    var communityId = document.getElementById("communityId").value;

    console.dir(postTypeId);
    console.dir(communityId);

    jQuery.ajax({
        type: "GET", url: "/getPostsOfPostType",
        data: {"pt_id": postTypeId, "cmn_id": communityId},
        async: false,
        success:
            function (result) {
                console.log(result);

                var postList = result.posts;
                var postTags = result.postTags;
                filterPosts(postList, postTags);

            },
        error:
            function (returnVal) {
                console.log(returnVal);
                if (returnVal.status === 404) {

                }

            }
    });
}

function filterPosts(postList, postTags) {

}