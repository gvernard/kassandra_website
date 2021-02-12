$(document).ready(function() {
    change_active_tab();
});
function change_active_tab(){
    var href = $(location).attr('href');
    var tabname = href.substring(href.lastIndexOf('/') + 1)

    $('.nav-link').removeClass('active_tab');
    if( tabname.length == 0 ){	
	$('.navbar-nav').find('a[href="predict"]').addClass('active_tab');	
    } else {
	$('.navbar-nav').find('a[href="'+tabname+'"]').addClass('active_tab');
    }
}
