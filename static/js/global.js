$(function(){

	$('form button').on('click', function(e){
		e.preventDefault();
	});

	$('form .file').on('change', function(){
		$(this).closest('form').submit();
	});

});

