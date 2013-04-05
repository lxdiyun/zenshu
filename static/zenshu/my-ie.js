$(document).ready(function(){
	$(".hover-div").hover(function(){
		$(this).css("background", "#f5f5f5");
	}, function(){
		$(this).css("background", "#fff");
	});
});


var shiftWindow = function() { scrollBy(0, -50) };
window.addEventListener("hashchange", shiftWindow);
function load() { if (window.location.hash) shiftWindow(); }
