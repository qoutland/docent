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
          $(str).find("span").fadeOut("fast")
          $(str).find("span").fadeIn()
          $(str).find("span").removeClass("glyphicon-star-empty").addClass("glyphicon-star");
        } else if (data == 'deleted') {
          $(str).find("span").fadeOut("fast")
          $(str).find("span").removeClass("glyphicon-star").addClass("glyphicon-star-empty");
          $(str).find("span").fadeIn()
        }
      },
    })
  });

  $('.removeLike').click(function () {
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
          if (data == 'deleted') {
          $(str).parent().parent().fadeOut()
        }
      },
    })
  });

  $('.addInt').click(function () {
    var catid;
    catid = $(this).attr("data-catid");
    $.ajax({
      type: "GET",
      url: "new_interest",
      data: {
        new_int: catid
      },
      success: function (data) {
        var str = "." + catid;
        console.log(data)
        if (data == 'created') {
          $(str).fadeIn()
          //this.parent().fadeOut()
        }
      },
    })
  });

  $('.removeInt').click(function () {
    var catid;
    catid = $(this).attr("data-catid");
    $.ajax({
      type: "GET",
      url: "new_interest",
      data: {
        new_int: catid
      },
      success: function (data) {
        var str = "." + catid;
        console.log(data)
        if (data == 'deleted') {
          $(str).fadeOut()
          //this.parent().fadeOut()
        }
      },
    })
  });