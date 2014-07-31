// Init foudnation library
$(document).foundation();

// Function of the site
$(document).ready(function() {
    $(".overlay").css("width", $(".loop-servicios").width());
    /* Initialise bxSlider */
    $('.bxslider').bxSlider({
        captions: true
    });
    //Apply img-thumbnail class to body-content images
    $('.body-content img').addClass("img-thumbnail");
});

// Resize function for the proyect hover
$(window).resize(function() {
    $(".overlay").css("width", $(".loop-servicios img").width());
});

