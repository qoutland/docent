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

//Showing categories when they are chosen (DOnt think this does anything rn)
$('.category').click(function (e) {
  $(this).addClass('active');
});

//Fades away like
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

//Initiates jumbotron animation
function animateJumbo() {
  $('.jumbo-text').fadeIn('slow')
}

//Add an interest (Still working on making this async)
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

//Fades away an interest after removing it
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

//Shows modals (might be able to remove)
$('.show_modal').click(function () {
  $('.modal').style.display = "block";
});

//Chooses email based on who user decides to contact
$("#contactLink").change(function() {
  if($(this).val() == "quin"){$("#contactForm").attr("action", "https://formspree.io/qoutland@gmail.com");
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

 var acts = document.getElementsByClassName('card-body');
 function showMap(position) {
     Array.from(acts).forEach((act) => {
         // Do stuff here
         act.getElementsByClassName('distance')[0].innerHTML = Math.round(distance(position.coords.latitude,position.coords.longitude,act.getElementsByClassName('latitude')[0]['defaultValue'],act.getElementsByClassName('longitude')[0]['defaultValue'])*10)/10 + ' mi';
     });
 }
 function distance(lat1, lon1, lat2, lon2) {
     var p = 0.017453292519943295;
     var c = Math.cos;
     var a = 0.5 - c((lat2 - lat1) * p)/2 + c(lat1 * p) * c(lat2 * p) * (1 - c((lon2 - lon1) * p))/2;
     return 12742 * Math.asin(Math.sqrt(a)) * 0.621371;
 }
 navigator.geolocation.getCurrentPosition(showMap);