queue()
    .defer(d3.json, "/charts/show_data")
    //.defer(d3.json, "static/geojson/us-states.json")
    .await(makeGraphs);

function makeGraphs(error, projectsJson, statesJson) {

	//Clean projectsJson data
	var resourceMonitoring = projectsJson;
	var dateFormat = d3.time.format("%M %d %HH %mm");
	resourceMonitoring.forEach(function(d) {
		d["date"] = dateFormat.parse(d["date"]);
		//d["date"].setDate(1);
		d["cpu_user"] = d["cpu"]['user'];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(resourceMonitoring);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["dt"]; });
	var cpuDim = ndx.dimension(function(d) { return d["cpu_user"];});
	//var povertyLevelDim = ndx.dimension(function(d) { return d["poverty_level"]; });
	//var stateDim = ndx.dimension(function(d) { return d["school_state"]; });
	//var totalDonationsDim  = ndx.dimension(function(d) { return d["total_donations"]; });


	//Calculate metrics
	var numProjectsByDate = dateDim.group();
	var cpuUsageByTime = cpuDim.group();
	//var numProjectsByPovertyLevel = povertyLevelDim.group();

  //var totalDonationsByState = stateDim.group().reduceSum(function(d) {
	//	return d["total_donations"];
	//});

	var all = ndx.groupAll();
	//var totalDonations = ndx.groupAll().reduceSum(function(d) {return d["total_donations"];});

	//var max_state = totalDonationsByState.top(1)[0].value;

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["dt"];
	var maxDate = dateDim.top(1)[0]["dt"];

    //Charts
	var timeChart = dc.barChart("#time-chart");
	//var resourceTypeChart = dc.rowChart("#resource-type-row-chart");
	//var povertyLevelChart = dc.rowChart("#poverty-level-row-chart");
	//var usChart = dc.geoChoroplethChart("#us-chart");
//	var numberProjectsND = dc.numberDisplay("#number-projects-nd");
//	var totalDonationsND = dc.numberDisplay("#total-donations-nd");

/*
	numberProjectsND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(all);

	totalDonationsND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(totalDonations)
		.formatNumber(d3.format(".3s"));
*/
	timeChart
		.width(600)
		.height(160)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(cpuDim)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.xAxisLabel("Time")
		.yAxis().ticks(4);
/*
	resourceTypeChart
        .width(300)
        .height(250)
        .dimension(resourceTypeDim)
        .group(numProjectsByResourceType)
        .xAxis().ticks(4);

	povertyLevelChart
		.width(300)
		.height(250)
        .dimension(povertyLevelDim)
        .group(numProjectsByPovertyLevel)
        .xAxis().ticks(4);


	usChart.width(1000)
		.height(330)
		.dimension(stateDim)
		.group(totalDonationsByState)
		.colors(["#E2F2FF", "#C4E4FF", "#9ED2FF", "#81C5FF", "#6BBAFF", "#51AEFF", "#36A2FF", "#1E96FF", "#0089FF", "#0061B5"])
		.colorDomain([0, max_state])
		.overlayGeoJson(statesJson["features"], "state", function (d) {
			return d.properties.name;
		})
		.projection(d3.geo.albersUsa()
    				.scale(600)
    				.translate([340, 150]))
		.title(function (p) {
			return "State: " + p["key"]
					+ "\n"
					+ "Total Donations: " + Math.round(p["value"]) + " $";
		})
*/
    dc.renderAll();

};
