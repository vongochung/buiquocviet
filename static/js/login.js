$(document).ready(function(){
	$(".img-login").click(function(){
	    $("#id_username").val($(this).data('name'));
	    $(".img-login img").removeClass('actived');
	    $(this).children("img").addClass('actived');
	});
});