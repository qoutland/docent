$('.likebutton').click(function () {
    var catid;
    catid = $(this).attr("data-catid");
    $.ajax({
      type: "GET",
      url: "save_act",
      data: {
        post_id: catid
      },
      success: function (data) {
        var str = "." + catid;
        if (data == 'created') {
          $(str).find("span").removeClass("glyphicon-star-empty").addClass("glyphicon-star");
          console.log("created")
        } else if (data == 'deleted') {
          $(str).find("span").removeClass("glyphicon-star").addClass("glyphicon-star-empty");
          console.log("deleted")
        }
      },
    })
  });