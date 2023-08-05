$('#slider1, #slider2, #slider3',).owlCarousel({
    loop: true,
    margin: 20, 
    
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        540: {
            items: 2,
            nav: true,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


$(document).ready(function(){
    $("#slider4").owlCarousel({
      items: 7,
      loop: true,
      dots: true,
      margin: 10,
      autoplay: true,
      autoplayTimeout: 3000,
      autoplayHoverPause: true,
      nav: false // Set nav to false to hide previous and next buttons
    });
  });
$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var quantityElement = $(this).parent().find('#quantity');
    
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("Received response from server:", data);
            quantityElement.text(data.quantity);
            document.getElementById("amount").innerText=data.amount
            document.getElementById("total").innerText=data.total
            if(data.quantity == 1){
                $('.minus-cart[pid="'+id+'"]').prop('disabled', true);
            } else {
                $('.minus-cart[pid="'+id+'"]').prop('disabled', false);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error while sending request:", textStatus, errorThrown);
        }
    });
});

$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var quantityElement = $(this).parent().find('#quantity');
    
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("Received response from server:", data);
            quantityElement.text(data.quantity);
            document.getElementById("amount").innerText=data.amount
            document.getElementById("total").innerText=data.total
            if(data.quantity == 1){
                $('.minus-cart[pid="'+id+'"]').prop('disabled', true);
            } else {
                $('.minus-cart[pid="'+id+'"]').prop('disabled', false);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error while sending request:", textStatus, errorThrown);
        }
    });
});
$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = $(this)
    
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            console.log("Received response from server:", data);
            
            // update amount and total variables
            var amount = data.amount;
            var total = data.total;
            
            // update HTML elements with new values
            document.getElementById("amount").innerText = amount;
            document.getElementById("total").innerText = total;
            eml.closest('.col-md-8').remove();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error while sending request:", textStatus, errorThrown);
        }
    });
});


var modal = document.getElementById("myModal");
  
  // Get the image and insert it inside the modal - use its "alt" text as a caption
  var img = document.getElementById("myImg");
  var modalImg = document.getElementById("img01");
  var captionText = document.getElementById("caption");
  img.onclick = function(){
    modal.style.display = "block";
    modalImg.src = this.src;
    captionText.innerHTML = this.alt;
  }
  
  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];
  
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() { 
    modal.style.display = "none";
  }  

 // slider 
 
 var productId = 123;  // replace with the actual product ID
 $.ajax({
   type: 'POST',
   url: '/wishlist/add/',
   data: {
     'prod_id': productId,
     csrfmiddlewaretoken: '{{ csrf_token }}'
   },
   success: function(response) {
     // handle success
   },
   error: function(xhr, textStatus, error) {
     // handle error
   }
 });


 
 var productId = 123;  // replace with the actual product ID
 $.ajax({
   type: 'POST',
   url: '/wishlist/add/',
   data: {
     'prod_id': productId,
     csrfmiddlewaretoken: '{{ csrf_token }}'
   },
   success: function(response) {
     // handle success
   },
   error: function(xhr, textStatus, error) {
     // handle error
   }
 });
   
  