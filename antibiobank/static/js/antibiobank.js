
// =============================================================
// Fonction principale qui récupere les données d'antibiogramme
// =============================================================
function get_stats(){

	/* Creation de la requete POST */
	send = {}
	send["bactery_id"]  = $("#bacteries_input").val();;
	send["specimen_id"] = $("#specimens_input").val();
	send["service_id"]  = $("#services_input").val();
	send["filter_mode"] = $("#filter_mode").val();
	send["filter_ids"] = [];
	$("#atb_list li.uk-active").each(function(){
		send["filter_ids"].push($(this).attr("value"));
	});

	
	$('#overlay').show();
	$("#atb_list").empty();
	$("#box_container").empty();


	var request = $.post("ajax_stats.json",send, function(results,status){
		
		load_atb(results)
		load_chart(results);
		$("#bactery_name").text(results.name);
		$("#total").text(results.total);


	});

	request.always(function(){$('#overlay').hide();});
	
	


}

// =============================================================
// Affiche la liste des antibiogramme disponnible 
// =============================================================
function load_atb(results){

	for (var i=0; i<results.data.length; i++)
		$("#atb_list").append("<li value="+results.data[i].id+"><a href='#'>"+results.data[i].name+"</a></li>")

}
// =============================================================
// Affiche les chart des antibiogramme disponnible 
// =============================================================
function load_chart(results){


	var strVar="";
	strVar += "<div class=\"uk-width-custom uk-grid-margin\" style=\"width:300px;display:none\" id=\"box_template\">";
	strVar += "					<div class=\"uk-panel uk-panel-box\" >";
	strVar += "<h4 class='atb_name'> {CHARTNAME}</h4>	";
	strVar += "						<div id=\"{CHARTID}\" style=\"height: 300px; width: 100%;\">";
	strVar += "						<\/div>";
	strVar += "					<\/div>";

	box_template = strVar;
	console.debug(results)

	for (var i=0; i<results.data.length; i+=1)
	{
		box = box_template.replace("display:none", "");
		box = box.replace("{CHARTID}", "chart-"+i);
		box = box.replace("{CHARTNAME}", results.data[i].name );

		if ($("#chart-"+i).length == 0)  // If existe deja, on refait pas
			$("#box_container").append(box);



		Morris.Donut({
			element: "chart-"+i,
			colors:["#98cb4a","#f26075","#849199" ],
			data: [
			{label: "S", value: results.data[i].S},
			{label: "R", value: results.data[i].R},
			{label: "I", value: results.data[i].I}
			]
		});





		// var chart = new CanvasJS.Chart("chart-"+i,
		// {
		// 	title:{
		// 		text: results.data[i].name + " (" + results.data[i].count +")",
		// 		fontSize: 14
		// 	},
		// 	legend:{
		// 		verticalAlign: "top",
		// 		horizontalAlign: "center"
		// 	},
		// 	data: [
		// 	{
		// 		type: "doughnut",
		// 		showInLegend:true,
		// 		dataPoints: [
		// 		{  y: results.data[i].S, indexLabel: "S", color:"#98cb4a", legendText:"Sensible"},
		// 		{  y: results.data[i].R ,indexLabel: "R" , color:"#f26075", legendText:"Resistant"},
		// 		{  y: results.data[i].I, indexLabel: "I" , color:"#849199", legendText:"Intermediaire"},

		// 		]
		// 	}
		// 	]
		// });

		// chart.render();

	}

}
// =============================================================
// Charge les listes
// =============================================================

function load_option(destination, url)
{
	$(destination).empty();

	$.getJSON(url, function(data) {
		for (var i=0; i<data.results.length; i+=1)
			$(destination).append("<option value='"+data.results[i].id+"'>"+data.results[i].name+"</option>")

	});

}


// =============================================================
// Function principale
// =============================================================

$(document).ready(function(){



// Morris.Donut({
//   element: 'myfirstchart',
//   data: [
//     {label: "Download Sales", value: 12},
//     {label: "In-Store Sales", value: 30},
//     {label: "Mail-Order Sales", value: 20}
//   ]
// });



// Lance la recherche 
$( "#getButton" ).click(function() {get_stats() });


$('#overlay').hide();


// Ajoute des filtres
$('#atb_list').on('click','li',function() {

	element =$(this);
	element.toggleClass("uk-active");

});



load_option("#bacteries_input", "ajax_bacteries.json");
// load_option("#services_input", "ajax_services.json");
// load_option("#specimens_input", "ajax_specimens.json");

});
