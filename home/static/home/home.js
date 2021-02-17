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
	"areas": {
            "FR": {
                "attrs": {
                    "fill": "#BF6E50"
                }
            },
            "US": {
                "attrs": {
                    "fill": "#BF3604"
                }
            }
        }
    });

});
