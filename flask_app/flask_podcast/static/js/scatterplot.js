
var w = 500;
var h = 500;
var padding = 30;
var radius = 5;

var xScale = d3.scale.linear()
					 .domain([d3.min(mds_data, function (d) { return d.x_coord; }),
					 		  d3.max(mds_data, function (d) { return d.x_coord; }) ])
					 .range([padding, w - padding * 2]);

var yScale = d3.scale.linear()
					 .domain([d3.min(mds_data, function (d) { return d.y_coord; }),
					 		  d3.max(mds_data, function (d) { return d.y_coord; }) ])
					 .range([h - padding, padding]);

<<<<<<< HEAD
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
=======
// var rScale = d3.scale.linear()
// 					 .domain([0, d3.max(mds_data, function (d) { return d[1]; })])
// 					 .range([2, 5]);
>>>>>>> 24be3cb... fix simserver clusterfuck

var svg = d3.select("#scatterplot")
			.append("svg")
			.attr("width", w)
			.attr("height", h);
>>>>>>> Stashed changes

svg.call(tip);


var circles = svg.selectAll("circle")
	.data(mds_data)
	.enter()
	.append("circle")
<<<<<<< HEAD
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
=======
	.attr("cx", function (d) { return xScale(d.x_coord); })
	.attr("cy", function (d) { return yScale(d.y_coord); })
	.attr("r",  radius)
	.style("fill", function (d) {
		var returnColor;
		if (d.searched === true) {
			returnColor = "red";
		} else {
			returnColor = "black";
		}
		return returnColor;
	});
	// .on("mouseover", function (d) { 
		
	// 	var xPosition = parseFloat(d3.select(this).attr("cx")) - 14;
	// 	var yPosition = parseFloat(d3.select(this).attr("cy")) - 14;
>>>>>>> 24be3cb... fix simserver clusterfuck

	// 	d3.select("#tooltip")
	// 		.style("left", xPosition + "px")
	// 		.style("top", yPosition + "px")
	// 		.select("#value")
	// 		.text(d)

	// 	d3.select("#tooltip").classed("hidden", false)

	// 	//make it big and red
	// 	d3.select(this)
	// 	 .transition()
	// 	 .duration(250)
	// 	 .attr("r", 10)
	// 	 .attr("fill", "red"); })

	// .on("mouseout", function (d) { 
	// 	d3.select("#tooltip").classed("hidden", true)

	// 	d3.select(this)
	// 		.transition()
	// 		.duration(250)
	// 		.attr("r", 5)
	// 		.attr("fill", "black") } );

// var textLabels = svg.selectAll("text")
// 	.data(mds_data)
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
