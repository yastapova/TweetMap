// Map visualization adapted from Michele Chandra's Basic US State Map Block
// http://bl.ocks.org/michellechandra/0b2ce4923dc9b5809922

var width = 1000;
var height = 500;

d3.select("svg").remove();

var projection = d3.geo.albersUsa()
	.translate([width/2, height/2])
	.scale([1000]);

var path = d3.geo.path()
	.projection(projection);

var svg = d3.select("div#map")
	.append("svg")
	.attr("width", width)
	.attr("height", height);

var colorscale = d3.scale.linear()
	.domain([-1.0, 0, 1.0])
	.range(["red", "white", "skyblue"]);

var tooltip = d3.select("body")
	    .append("div")   
		.attr("class", "tooltip")               
		.style("opacity", 0);

d3.json("static/us-states.json", function(json) {
	d3.csv("static/map_data.csv", function(dat) {
		for(var i = 0; i < json.features.length; i++)
		{
			var jState = json.features[i].properties.abbrev;
			json.features[i].properties.sentiment = -10;

			for(var j = 0; j < dat.length; j++)
			{
				var datState = dat[j].state;
				var datSent = dat[j].sentiment;

				if(datState == jState)
				{
					json.features[i].properties.sentiment = datSent;
					break;
				}
			}
		}

	svg.selectAll("path")
		.data(json.features)
		.enter()
		.append("path")
		.attr("d", path)
		.attr("id", function(d) {
			return "state_" + d.properties.abbrev;
		})
		.attr("value", function(d) {
			return d.properties.sentiment;
		})
		.style("stroke", "#000")
		.style("stroke-width", "1")
		.style("fill", function(d) {
			var sent = parseFloat(d.properties.sentiment);
			if(sent == -10) {
				return "gray";
			} else {
				return colorscale(sent);
			}
		})
		.on("mouseover", function(d) {
			var txt = d.properties.abbrev + ": ";
			if(d.properties.sentiment == -10) {
				txt = txt + "N/A"
			} else {
				txt = txt + parseFloat(d.properties.sentiment).toFixed(5);
			}
			d3.select(this)
				.style("stroke", "magenta")
				.style("stroke-width", "6");

			tooltip.transition()
	      	   .duration(200)      
	           .style("opacity", .9);      
           	tooltip.text(txt)
	           .style("left", (d3.event.pageX) + "px")     
	           .style("top", (d3.event.pageY - 28) + "px"); 
		})
		.on("mouseout", function(d) {
			d3.select(this)
				.style("stroke", "#000")
				.style("stroke-width", "1");

			tooltip.transition()        
	           .duration(500)      
	           .style("opacity", 0);
		});
	})
});
