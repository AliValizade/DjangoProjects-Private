
$(".owl-carousel").owlCarousel({
	autoplay:false,
	autoplayhoverpause:true,
	autoplaytimout:100,
	items: 5,
	nav:true,
	animateIn: 'flipInY',
	animateOut: 'zoomOutDown',
	responsive: {
		0 : {
			items: 1,
			dots: false
		},
		485 : {
			items: 2,
			dots: false
		},
		728 : {
			items: 3,
			dots: false
		},
		960 : {
			items: 4,
			dots: true
		},
		1280 : {
			items: 5,
			dots: true
		},
	}
});