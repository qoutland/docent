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
          console.log("created")
          $(str).find("i").fadeOut("fast")
          $(str).find("i").fadeIn()
          $(str).find("i").removeClass("fa-star-o").addClass("fa-star");
        } else if (data == 'deleted') {
          $(str).find("i").fadeOut("fast")
          $(str).find("i").removeClass("fa-star").addClass("fa-star-o");
          $(str).find("i").fadeIn()
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

  $('.show_modal').click(function () {
    $('.modal').style.display = "block";
  });