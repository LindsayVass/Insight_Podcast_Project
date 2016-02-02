var dataset = [
[5,20], 
[480,90], 
[250,50], 
[100,33], 
[330,95],
[410,12], 
[475,44],
[25,67], 
[85,21], 
[220,88],
[600, 160]
];

var w = 400;
var h = 400;
var padding = 30;

var xScale = d3.scale.linear()
					 .domain([0, d3.max(dataset, function (d) { return d[0]; })])
					 .range([padding, w - padding * 2]);

var yScale = d3.scale.linear()
					 .domain([0, d3.max(dataset, function (d) { return d[1]; })])
					 .range([h - padding, padding]);

<<<<<<< Updated upstream
var rScale = d3.scale.linear()
					 .domain([0, d3.max(dataset, function (d) { return d[1]; })])
					 .range([2, 5]);
=======
var tip = d3.tip()
	.attr('class', 'd3-tip')
	.offset([-10, 0])
	.html(function(d) {
		return d.name;
	});

var svg = d3.select("#scatterplot")
			.append("svg")
			.attr("width", w)
			.attr("height", h);
>>>>>>> Stashed changes

svg.call(tip);


var circles = svg.selectAll("circle")
	.data(dataset)
	.enter()
	.append("circle")
<<<<<<< Updated upstream
	.attr("cx", function (d) { return xScale(d[0]); })
	.attr("cy", function (d) { return yScale(d[1]); })
	.attr("r",  function (d) { return rScale(d[1]); })
	.on("mouseover", function (d) { 
		
		var xPosition = parseFloat(d3.select(this).attr("cx")) - 14;
		var yPosition = parseFloat(d3.select(this).attr("cy")) - 14;
=======
	.attr("cx", function (d) { return xScale(d.x_coord); })
	.attr("cy", function (d) { return yScale(d.y_coord); })
	.attr("r",  radius)
	.style("fill", function (d) {
			var returnColor;
			if (d.searched === true) {
				returnColor = "#8C3FC6";
			} else {
				returnColor = "black";
			}
			return returnColor;
		})
	.on("mouseover", tip.show)
	.on("mouseout", tip.hide);



	// .on("mouseover", function (d) {
	// 	//get position
	// 	var xPosition = parseFloat(d3.select(this).attr("cx"));
	// 	var yPosition = parseFloat(d3.select(this).attr("cy"));

	// 	//create tooltip
	// 	svg.append("text")
	// 		.attr("id", "tooltip")
	// 		.attr("x", xPosition)
	// 		.attr("y", yPosition)
	// 		.attr("text-anchor", "middle")
	// 		.attr("font-family", "sans-serif")
	// 		.attr("font-size", "11px")
	// 		.attr("font-weight", "bold")
	// 		.attr("fill", "black")
	// 		.text()
	// })





		// .append("div tooltip")
		// .on("mouseover", function (d) { return tooltip.style("visibility")})
	// .on("mouseover", function (d) { 
		
	// 	var xPosition = parseFloat(d3.select(this).attr("cx"));
	// 	var yPosition = parseFloat(d3.select(this).attr("cy"));

	// 	// create the tooltip label
	// 	svg.append("title")
	// 		.attr("id", "tooltip")
	// 		.attr("x", xPosition)
	// 		.attr("y", yPosition)
	// 		.attr("text-anchor", "middle")
	// 		.attr("font-family", "sans-serif")
	// 		.attr("font-size", "11px")
	// 		.attr("font-weight", "bold")
	// 		.attr("fill", "black")
	// 		.text(function(d) { return d.name; })

	// })
	// .on("mouseout", function() {
	// 	//remove the tooltip
	// 	d3.select("#tooltip").remove();
	// });
>>>>>>> Stashed changes

		d3.select("#tooltip")
			.style("left", xPosition + "px")
			.style("top", yPosition + "px")
			.select("#value")
			.text(d)

		d3.select("#tooltip").classed("hidden", false)

		//make it big and red
		d3.select(this)
		 .attr("r", 10)
		 .attr("fill", "red"); })

	.on("mouseout", function (d) { 
		d3.select("#tooltip").classed("hidden", true)

		d3.select(this)
			.transition()
			.duration(250)
			.attr("r", rScale(d[1]))
			.attr("fill", "black") } );

// var textLabels = svg.selectAll("text")
// 	.data(dataset)
// 	.enter()
// 	.append("text")
// 	.text(function (d) { return d[0] + "," + d[1];})
// 	.attr("x", function (d) { return xScale(d[0]); })
// 	.attr("y", function (d) { return yScale(d[1]); })
// 	.attr("font-family", "sans-serif")
// 	.attr("font-size", "11px")
// 	.attr("fill", "red")
// 	.style("pointer-events", "none");

// svg.append("g")
//    .attr("class", "axis")
//    .attr("transform", "translate(0," + (h - padding) + ")")
//    .call(xAxis);

// svg.append("g")
//    .attr("class", "axis")
//    .attr("transform", "translate(" + padding + ",0)")
//    .call(yAxis);
