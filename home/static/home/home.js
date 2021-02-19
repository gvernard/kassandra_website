var blues = ["#6ECBD4","#3EC7D4","#028E9B","#01565E"]
var pinks = ["#E39AC3","#DA5BB2","#C72289","#ED00AE"]
var mycolors = pinks

$(document).ready(function(){
    $(".mapcontainer").mapael({
        "map": {
            "name" : "world_countries",
	    "zoom": {
		"enabled": true,
		"maxLevel": 10
            },
	    "defaultArea": {
                "attrs": {
                    "fill": "#6cbad9",
                    "stroke": "#0388A6",
		    "stroke-width": 0.3
                },
                "attrsHover": {
                    "fill": "#f38a03"
                }
            }
        },
        legend: {
            area: {
                display: true,
                title: "New Cases:",
                marginBottom: 7,
                slices: [
                    {
                        max: 100,
                        attrs: {
                            fill: mycolors[0]
                        },
                        label: "Less than 100"
                    },
                    {
                        min: 100,
                        max: 1000,
                        attrs: {
                            fill: mycolors[1]
                        },
                        label: "Between 100 and 1k"
                    },
                    {
                        min: 1000,
                        max: 10000,
                        attrs: {
                            fill: mycolors[2]
                        },
                        label: "Between 1k and 10k"
                    },
                    {
                        min: 10000,
                        attrs: {
                            fill: mycolors[3]
                        },
                        label: "More than 10k"
                    }
                ]
            }
	}
    });

    $('#id_model').on("change",function(){
	get_new_cases();
    });

    get_new_cases();
});

function get_new_cases(){
    var form = $('#myform');
    
    $.ajax({
	url: "get_global_new_cases",
	data: form.serialize(),
	dataType: 'json',
	async: false,
	success: function(response){
	    var updatedOptions = {'areas': {}};
	    for(var key in response){
		updatedOptions.areas[key] = {
		    value: response[key],
		    href: '/predict/?country='+code_match[key]+'&start_date=2021-05-01&end_date=2021-05-20&model_field='+$('#id_model').val(),
		    tooltip:{
			content: '<table><tr><td colspan="2" style="font-weight:bold;text-align:center">'+key+'</td></tr><tr><td>New Cases:</td><td>'+response[key]+'</td></tr></table>',
		    }
		}
	    }
	    var options = [{mapOptions: updatedOptions,animDuration: 1000}];
	    $(".mapcontainer").trigger('update',options)

	    if( $(".mapcontainer").css("visibility") === 'hidden' ){
		$(".mapcontainer").css('visibility','visible').hide().fadeIn();
	    }

	}
    });

}
