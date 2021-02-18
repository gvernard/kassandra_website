var countries;
var regions;

Chart.plugins.register({
    beforeDraw: function (chart, easing) {
        if (chart.config.options.chartArea && chart.config.options.chartArea.backgroundColor) {
            var ctx = chart.chart.ctx;
            var chartArea = chart.chartArea;
	    
            ctx.save();
            ctx.fillStyle = chart.config.options.chartArea.backgroundColor;
            ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
            ctx.restore();
        }
    }
});


$(document).ready(function() {
    $.ajax({
	url: "get_countries_and_regions",
	async: false,
	success: function(response){
	    countries = response["countries"];
	    regions = response["regions"];	    
	}
    });

    
    $('.datepicker').datepicker({dateFormat:'yy-mm-dd'});

    // Properties for the country field
    $("#id_country").autocomplete({
	source: countries,
	minLength: 0,
	select: function( event, ui ) {
	    $('#id_country').val(ui.item.value);
	    $('.ips_buttons').removeClass('active_button');
	    var txt = 'Latest enforced';
	    $('#but_hist').html(txt);
	    check_regions(ui.item.value);
	    change_ip_colors();
	}
    });

    $("#id_country").on("focus",function(){
	if( $(this).val().length > 0 ){
	    $(this).val('');
	}
	$("#id_country").autocomplete("search");
    });

    $('#id_country').on("change",function(){
	var country = $(this).val();
	if( !countries.includes(country) ){
	    $(this).val('');
	}
    });


    // Properties for the region field
    $("#id_region").on("focus",function(){
	if( $(this).val().length > 0 ){
	    $(this).val('');
	}
	$("#id_region").autocomplete("search");
    });
    
    $('#id_region').on("change",function(){
	var country = $('#id_country').val();
	var region = $(this).val();
	if( !regions[country].includes(region) ){
	    $(this).val('');
	}
    });


    
    





    
    
    

    mycolor  = 'rgb(255, 99, 132)'
    mycolor2 = 'rgba(255, 99, 132, 0.3)'
    mycolor3 = 'rgba(255, 99, 132, 0.7)'

    //mycolor = 'rgb(54, 162, 235)'
    var config = {
	type: 'line',
	options: {
	    chartArea: {
		backgroundColor: '#fcfaf2'
	    },
	    responsive: false,
	    title: {
		display: true,
		text: "Kassandra's prediction",
		fontSize: 24,
		fontStyle: 'italic'
	    },
	    tooltips: {
		mode: 'index',
		intersect: false,
	    },
	    hover: {
		mode: 'nearest',
		intersect: true
	    },
	    scales: {
		xAxes: [{
		    display: true,
		    type: 'time',
		    scaleLabel: {
			display: true,
			labelString: 'Time'
		    },
		    time: {
			unit: 'week'
		    }
		}],
		yAxes: [{
		    display: true,
		    scaleLabel: {
			display: true,
			labelString: 'New Cases'
		    }
		}]
	    }
	}
    };
    Chart.defaults.global.defaultFontSize = 18;
    var ctx = document.getElementById('myChart').getContext('2d');
    window.myLine = new Chart(ctx, config);


    $("#but_predict").click(function(){
	if( !$('#id_country').val() ) {
	    alert('Country name required!');
	    $('#id_country').focus();
	    return;
	}
	if( !$('#id_rate').val() ) {
	    alert('Rate value required!');
	    $('#id_rate').focus();
	    return;
	}
	if( !$('#id_start_date').val() ) {
	    alert('Start date required!');
	    $('#id_start_date').focus();
	    return;
	}
	if( !$('#id_end_date').val() ) {
	    alert('End date required!');
	    $('#id_end_date').focus();
	    return;
	}

	var form = $(this).closest("form");
	var start_date = new Date( form.find("input[name='start_date']").val() );
	var end_date = new Date( form.find("input[name='end_date']").val() );

	if( start_date >= end_date ){
	    alert("Error: start date should be before the end date.");
	    return;
	}
	
	$.ajax({
	    url: form.attr("form-url"),
	    data: form.serialize(),
	    dataType: 'json',
	    success: function(response){
		//alert(response["IP_vector"]);
		
		// Remove last dataset
		config.data.datasets.splice(0,3);
		
		// Add the new datasets
		var quant75 = {
		    label: '75%',
		    backgroundColor: mycolor2,
		    borderColor: mycolor3,
		    data: response["quant75"],
		    fill: '+2',
		    pointRadius: 0
		};
		config.data.datasets.push(quant75);
		var newCases = {
		    label: 'New cases',
		    backgroundColor: mycolor,
		    borderColor: mycolor,
		    data: response["newCases"],
		    fill: false
		};
		config.data.datasets.push(newCases);
		var quant25 = {
		    label: '25%',
		    backgroundColor: mycolor2,
		    borderColor: mycolor3,
		    data: response["quant25"],
		    fill: '-2',
		    pointRadius: 0
		};
		config.data.datasets.push(quant25);
		
		window.myLine.update();
	    }
	});

    });


    
    $("#myip_table tr:nth-child(odd)").append(function(){
	return $(this).next().remove().contents();
    });
    $('#myip_table').find('tr').each(function(){
        var slider = $(this).find('td').eq(0).find('input');
	var id = slider.attr('id');

	slider.on("change",function(){
	    $('.ips_buttons').removeClass('active_button');
	    $('#but_hist').html('Latest enforced');
	    $(this).parent().parent().find('td').eq(1).find('input').val($(this).val());
	});
	
	$('#'+id).on('input',function(){
	    $(this).parent().parent().find('td').eq(1).find('input').val($(this).val());
	});
    });
    $(".ips_div").fadeIn();



    
    
    $("#but_maxout").click(function(){
	$('#myip_table').find('tr').each(function(){
            var slider = $(this).find('td').eq(0).find('input');
	    var max = slider.attr('max');
	    slider.val(max);
	    slider.parent().parent().find('td').eq(1).find('input').val(max);
	});
	$('.ips_buttons').removeClass('active_button');
	$(this).addClass('active_button');
    });

    $("#but_min").click(function(){
	$('#myip_table').find('tr').each(function(){
            var slider = $(this).find('td').eq(0).find('input');
	    var min = slider.attr('min');
	    slider.val(min);
	    slider.parent().parent().find('td').eq(1).find('input').val(min);
	});
	$('.ips_buttons').removeClass('active_button');
	$(this).addClass('active_button');
    });

    
    $("#but_random").click(function(){
	$('#myip_table').find('tr').each(function(){
            var slider = $(this).find('td').eq(0).find('input');
	    var min = slider.attr('min');
	    var max = slider.attr('max');
	    var myval = getRandomInt(min,max);
	    slider.val(myval);
	    slider.parent().parent().find('td').eq(1).find('input').val(myval);
	});
	$('.ips_buttons').removeClass('active_button');
	$(this).addClass('active_button');
    });


    $("#but_hist").click(function(){
	if( !$('#id_country').val() ) {
	    alert('Country name required!');
	} else {	
	    var form = $(this).closest("form"); // Only need the geo
	    var but = $(this);

	    $.ajax({
		url: "get_latest_ips",
		data: form.serialize(),
		dataType: 'json',
		success: function(response){
		    //alert(response["date"]+'  '+response["ips"].join('-'));
		    //alert(response["geo"]);
		    
		    var hist_ips = response["ips"];
		    $('#myip_table').find('tr').each(function(index){
			var slider = $(this).find('td').eq(0).find('input');
			var myval = hist_ips[index]
			slider.val(myval);
			slider.parent().parent().find('td').eq(1).find('input').val(myval);
		    });
		    
		    but.html('Latest enforced ('+response["date"]+')');

		}
	    });

	    $('.ips_buttons').removeClass('active_button');
	    $(this).addClass('active_button');

	}
    });





    

    $("#id_model_field").on("change",function(){
	change_ip_colors();
    });


    
    $("#id_region").prop("disabled",true).val('');
    $("#but_hist").addClass("active_button");
    change_ip_colors();
    $("#but_predict").trigger("click");    
});




function change_ip_colors(){
    // I need the geo and the model name to find the model coefficients
    $.ajax({
	url: "get_model_colors",
	data: $('form').serialize(),
	dataType: 'json',
	async: false,
	success: function(response){
	    colors = response["colors"];
	    $('#myip_table').find('tr').each(function(index){
		$(this).find('label').parent().css('background-color',colors[index]);//.css('background','linear-gradient(0deg, rgba(58,180,75,0) 0%,'+colors[index]+' 50%, rgba(252,176,69,0) 100%)');
	    });
	}
    });
}

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function check_regions(country){
    if( regions[country].length == 0 ){
	$("#id_region").val('');
	$("#id_region").prop("disabled",true);
	//$("#id_region").autocomplete("destroy");
    } else {
	$("#id_region").prop("disabled",false);
	$("#id_region").autocomplete({
	    source: regions[country],
	    minLength: 0,
	    select: function( event, ui ) {
		$('#id_region').val(ui.item.value);
		$('.ips_buttons').removeClass('active_button');
		var txt = 'Latest enforced';
		$('#but_hist').html(txt);
		change_ip_colors();
	    }
	});
    }
};
