

var width = 500;
var height = 500;
var padding = 30;
var radius = 5;

var regularColor = "#FFFFFF";
var specialColor = "#000000";
var linkColor = "#abc915";
var json_error = "";
if (json_error) {
	var svg = d3.select("#scatterplot")
	.append("svg")
	.attr("width", width)
	.attr("height", height)
	.append("text")
	.attr("x", width/2)
	.attr("y", height/2)
	.text("Oops something went wrong.")
} else {



// Assign mds_data to nodes
var nodes = mds_data;

// Set up links
var links = []
for (var i = 1; i < nodes.length; i++)
	links.push({source: 0, 
				target: i, 
				similarity: nodes[i].similarity});


// Set up SVG container
var svg = d3.select("#scatterplot").append('svg')
	.attr("xmlns", "http://www.w3.org/2000/svg")
	.attr("width", width)
	.attr("height", height)
	.attr("id", "graph")
	.attr("viewBox", "0 0 " + width + " " + height)
	.attr("preserveAspectRatio", "xMidYMid meet");


// Set up a 2nd svg to hold description
var par = d3.select("#podcast-description")
	.append("div");

// Create force layout object
var force = d3.layout.force()
	.size([width, height])
	.nodes(nodes)
	.links(links);


// Specify link distance  - more similar podcasts have shorter distances
force.linkDistance( function(link) {
	return 1 - link.similarity;
});


// Specify link strength - more similar podcasts have stronger links
force.linkStrength( function(link) {
	return link.similarity;
});

// Add a charge to the nodes so they repel each other
force.charge(-400);

// Use gravity to keep the nodes centered in the visualization
force.gravity(0.4);

// Build the links and nodes (nodes come after so they show up on top)
var link = svg.selectAll(".link")
	.data(links)
	.enter().append("line")
	.attr("class", "link");

var node = svg.selectAll(".node")
	.data(nodes)
	.enter().append("circle")
	.attr("class", "node");

// link rows to nodes
var rows = d3.selectAll("tr")
.on("mouseover", function (d) {
	var rowId = d3.select(this).attr("id");
	d3.select("circle#node" + rowId)
		.transition()
		.duration(500)
		.style("fill", specialColor)
		.style("stroke", "white")
		.attr("r", width/50)

	var matchingNode = d3.select("#node" + rowId);
	var nodeData = matchingNode[0][0].__data__;
	
	//console.log(nodeData.name);

	$("#podcast-description").html("<strong>" + nodeData.name + 
		"</strong><br>" + nodeData.summary);
})
.on("mouseout", function (d) {
	var rowId = d3.select(this).attr("id");
	d3.select("circle#node" + rowId)
		.transition()
		.duration(500)
		.style("fill", regularColor)
		.style("stroke", "black")
		.attr("r", width/100)
	var matchingNode = d3.select("#node" + rowId);
});

// Define a function to call when force layout is calculating
force.on("tick", function() {
	
	// update position of nodes
	node.attr("r", width / 100)
		.attr("cx", function(d) { return d.x; })
		.attr("cy", function(d) { return d.y; })
		.attr("name", function(d) { return d.name; })
		.attr("summary", function(d) { return d.summary; })
		.attr("id", function(d) { return "node" + d.id; })
		.attr("searched", function(d) { return d.searched; })
		.style("stroke", "black")
		.style("fill", function (d) {
		var returnColor;
		if (d.searched === true) {
			returnColor = specialColor;
		} else {
			returnColor = regularColor;
		}
		return returnColor;
		})

	// update position of links
	link.attr("x1", function(d) { return d.source.x; })
		.attr("y1", function(d) { return d.source.y; })
		.attr("x2", function(d) { return d.target.x; })
		.attr("y2", function(d) { return d.target.y; })
		.attr("stroke-width", 1)
		.attr("stroke", linkColor);
});

force.start();

}

// Make sure description doesn't go below bottom of window
$( document ).ready(function() {
  $('#podcast-description').height(function(index, height) {
  	var newHeight = window.innerHeight - $(this).offset().top - 50;
  	// console.log("window.innerheight " + window.innerHeight);
  	// console.log("this.offset" + $(this).offset().top);
  	// console.log("newheight " + newHeight);
    $(this).css('height', newHeight);
  });
});