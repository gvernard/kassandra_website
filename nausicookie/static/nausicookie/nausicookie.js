$(function() {
    var arr = [];
    for(i=1;i<9;i++){
	for(var j=1;j<7;j++){
	    arr.push(String(i)+String(j));
	}
    }
    winningString = arr.join(',');

    
    $("#sortable").sortable({
	opacity: 0.6,
	cursor: 'move',
	update: function() {
            var currentString = '';
            $('#sortable li').each(function(){
		var imageId = $(this).attr("id");
		currentString += imageId.replace("recordArr_", "")+",";
            });
            currentString = currentString.substr(0,(currentString.length) -1);
            if(currentString == winningString){
		alert("Well done, you've won!");
		$("#sortable").remove();
		$("#true_img").show().fadeOut(4000,function() {
		    var new_src = $('#prize_img').attr("src");
		    $(this).hide().attr("src",new_src);
		    $(this).fadeIn(4000);
		}); 
            }
        }
    });
});
