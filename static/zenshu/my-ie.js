$(document).ready(function(){
	$(".hover-div").hover(function(){
		$(this).css("background", "#f5f5f5");
	}, function(){
		$(this).css("background", "#fff");
	});
});
