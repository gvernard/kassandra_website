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
                    "stroke": "#0388A6"
                },
                "attrsHover": {
                    "fill": "#f38a03"
                }
            }
        },
        legend: {
            area: {
                display: true,
                title: "New Cases",
                marginBottom: 7,
                slices: [
                    {
                        max: 100,
                        attrs: {
                            fill: "#6ECBD4"
                        },
                        label: "Less than 100"
                    },
                    {
                        min: 100,
                        max: 1000,
                        attrs: {
                            fill: "#3EC7D4"
                        },
                        label: "Between 100 and 1k"
                    },
                    {
                        min: 1000,
                        max: 10000,
                        attrs: {
                            fill: "#028E9B"
                        },
                        label: "Between 1k and 10k"
                    },
                    {
                        min: 10000,
                        attrs: {
                            fill: "#01565E"
                        },
                        label: "More than 10k"
                    }
                ]
            }
	}
    });





    
    $('#dum').on("click",function(){

	$.ajax({
	    url: "get_global_new_cases",
	    async: false,
	    success: function(response){
		var updatedOptions = {'areas': {}};
		for(var key in response){
		    updatedOptions.areas[key] = {
			value: response[key],
			tooltip: {
			    content: '<span style="color:blue"> '+response[key]+'</span>'
			}
		    }
		}
		$(".mapcontainer").trigger('update',
					   [{
					       mapOptions: updatedOptions,
					       animDuration: 1000
					   }]
					  );

	    }
	});


    });

});
