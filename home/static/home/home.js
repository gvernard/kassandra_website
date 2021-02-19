var blues = ["#6ECBD4","#3EC7D4","#028E9B","#01565E"]
var pinks = ['#FF8FCE','#F7549E','#FF2589','#FF0059']
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
		country_name = response[key]['CountryName'],
		newcases = response[key]['PredictedDailyNewCases'],
		quant25  = response[key]['PredictedDailyQuantile25'],
		quant75  = response[key]['PredictedDailyQuantile75'],
		updatedOptions.areas[key] = {
		    value: newcases,
		    href: '/predict/?country='+country_name+'&start_date='+$('#id_start_date').val()+'&end_date='+$('#id_end_date').val()+'&model_field='+$('#id_model').val(),
		    tooltip:{
			content: '<table><tr><td colspan="2" style="font-weight:bold;text-align:center">'+country_name+'</td></tr><tr><td>New Cases:</td><td>'+newcases+'</td></tr><tr><td>Uncertainty:</td><td>'+quant25+'-'+quant75+'</td></tr></table>',
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
