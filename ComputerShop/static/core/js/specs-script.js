$(document).ready(function(){
	let container = $('.specifications');
	let specs = $('.specs-footer');
	let table = $('.spec-table');
	const short = $('.detail-specs').height()
	let animationTime = parseInt(parseFloat($('.specs-footer i').css('transition-duration').slice(0, -1))*500)

	$(specs).click(function () {
		if (container.height() <= 220){
			container.animate({'height': container.height() - $('.detail-specs').height() + table.height() + 'px'}, animationTime);
			$('.specs-footer i').css('transform', 'rotate(180deg)')
		} else {
			container.animate({'height':container.height() - table.height() + short + 'px'}, animationTime)
			$('.specs-footer i').css('transform', 'rotate(0deg)')
		}
	})
})