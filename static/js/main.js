// Init foudnation library
$(document).foundation();

// Function of the site
$(document).ready(function() {
    /* Initialise bxSlider */
    $('.bxslider').bxSlider({
        captions: true,
	pager: false,
	controls: false,
	auto: true,
	slideWidth: 780,
    });
    $('.bxslider-services').bxSlider({
        captions: true,
	pager: false,
	controls: true,
	minSlides: 4,
	maxSlides: 4,
	slideWidth: 200,
    });
});
