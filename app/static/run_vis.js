var width = 1000;
var height = 500;

var projection = d3.geo.albersUsa()
					.translate([width/2, height/2])
					.scale([1000]);

var path = d3.geo.path()
			.projection(projection);

var svg = d3.select("div#map")
			.append("svg")
			.attr("width", width)
			.attr("height", height);

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
		.style("stroke", "#fff")
		.style("stroke-width", "1");
	})
});
