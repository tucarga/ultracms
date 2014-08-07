// Init foudnation library
$(document).foundation();

// Function of the site
$( window ).ready(function() {
    $(".overlay").css("width", $(".loop-servicios").width());
});

// Resize function for the proyect hover
$( window ).resize(function() {
    $(".overlay").css("width", $(".loop-servicios img").width());
});
