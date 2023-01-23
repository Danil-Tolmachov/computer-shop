$(document).ready(function(){

	$('.main-block').css('height', $('.products-inner').outerHeight());

	let container = document.querySelector('.products-inner');
	let filter = document.querySelectorAll('.filters-border');
	document.querySelector('.products-inner').style.borderTopLeftRadius = '0px';
	
	if (container.height > filter.height) {
		document.querySelector('.products-inner').style.borderBottomLeftRadius = '0px';
	}


	function hasClass(el, cls) {
			if (el.className.match('(?:^|\\s)'+cls+'(?!\\S)')) { return true; } 
			}
	function addClass(el, cls) {
			if (!el.className.match('(?:^|\\s)'+cls+'(?!\\S)')) { el.className += ' '+cls; } 
			}
	function delClass(el, cls) {
			el.className = el.className.replace(new RegExp('(?:^|\\s)'+cls+'(?!\\S)'),'');
			}

	function elementFromTop() {
		elem = document.querySelectorAll('.filters-border');
		products = document.querySelector('.products-inner');
		classToAdd = 'filters-border-triggered';
		distanceFromTop = 83;
		unit = 'pixels';

		let winY = window.innerHeight || document.documentElement.clientHeight, 
		elemLength = elem.length, distTop, distPercent, distPixels, distUnit, i;
		for (i = 0; i < elemLength; ++i) {
			distTop = elem[i].getBoundingClientRect().top;
			distPercent = Math.round((distTop / winY) * 100);
			distPixels = Math.round(distTop);
			distUnit = unit == 'percent' ? distPercent : distPixels;
			if (distUnit <= distanceFromTop) {
				if (!hasClass(elem[i], classToAdd)) { 
					addClass(elem[i], classToAdd);

					products.style.borderTopLeftRadius = '12px';
					products.style.transition = '0.05s';

					if (products.clientHeight = 700) {
						products.style.borderBottomLeftRadius = '12px';
					}
				}
			} else {
				delClass(elem[i], classToAdd);
				products.style.borderTopLeftRadius = '0px';
				products.style.borderBottomLeftRadius = '12px';
			}
			}
		}

	window.addEventListener("scroll", elementFromTop);

})