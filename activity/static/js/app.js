//Function to handle saving activities without refreshing page
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
      var str = ".mark_" + catid;
      if (data == 'created') {
        $(str).find("i").fadeOut("fast")
        $(str).find("i").fadeIn()
        $(str).find("i").removeClass("far fa-bookmark").addClass("fas fa-bookmark");
      } else if (data == 'deleted') {
        $(str).find("i").fadeOut("fast")
        $(str).find("i").removeClass("fas fa-bookmark").addClass("far fa-bookmark");
        $(str).find("i").fadeIn()
      }
    },
  })
});

$('.category').click(function (e) {
  $(this).addClass('active');
});

$('.removelike').click(function () {
  var catid;
  catid = $(this).attr("data-catid");
  $.ajax({
    type: "GET",
    url: "save_act",
    data: {
      post_id: catid
    },
    success: function (data) {
      var str = ".mark_" + catid;
      if (data == 'deleted') {
        $(str).parent().parent().fadeOut("fast")
      }
    },
  })
});

function animateJumbo() {
  $('.jumbo-text').fadeIn('slow')
}

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
      var str = ".butt_" + catid;
      console.log(data)
      if (data == 'deleted') {
        console.log(str)
        $(str).fadeOut()
        //this.parent().fadeOut()
      }
    },
  })
});

$('.show_modal').click(function () {
  $('.modal').style.display = "block";
});

$("#contactLink").change(function() {
  if($(this).val() == "quin"){
    $("#contactForm").attr("action", "https://formspree.io/qoutland@gmail.com");
  }
  else if($(this).val() == "sophia"){
    $("#contactForm").attr("action", "https://formspree.io/sophia3587@gmail.com");
  }
  else if($(this).val() == "kevin"){
    $("#contactForm").attr("action", "https://formspree.io/kevinbenjamin@nevada.unr.edu");
  }
  else if($(this).val() == "all"){
    $("#contactForm").attr("action", "https://formspree.io/qoutland@gmail.com");
    $("#contactCC").attr("value", "sophia3587@gmail.com,kevinbenjamin@nevada.unr.edu");
  }
 });