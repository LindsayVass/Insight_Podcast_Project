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


var tip = d3.tip()
	.attr('class', 'd3-tip')
	.direction('s')
	.offset([10, 0])
	.html(function(d) {
		return "<strong>" + d.name + "</strong><br>" + d.summary;
	});

var svg = d3.select("#scatterplot")
			.append("svg")
			.attr("width", w)
			.attr("height", h);

svg.call(tip);


var circles = svg.selectAll("circle")
	.data(mds_data)
	.enter()
	.append("a")
		.attr("xlink:href", function (d) {
			return "../output?id=" + d.id;
		})
	.append("circle")
	.attr("cx", function (d) { return xScale(d.x_coord); })
	.attr("cy", function (d) { return yScale(d.y_coord); })
	.attr("r", radius)
	.style("fill", function (d) {
		var returnColor;
		if (d.searched === true) {
			returnColor = "#9900cc";
		} else {
			returnColor = "black";
		}
		return returnColor;
	})

	.on("mouseover", tip.show)
	.on("mouseout", tip.hide)
	;





