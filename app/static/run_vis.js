// Map visualization adapted from Michele Chandra's Basic US State Map Block
// http://bl.ocks.org/michellechandra/0b2ce4923dc9b5809922

var width = 1000;
var height = 500;

// Clear canvas before loading new data
d3.select("svg").remove();

// Map definition
var projection = d3.geo.albersUsa()
    .translate([width/2, height/2])
    .scale([1000]);

// Drawing the map
var path = d3.geo.path()
    .projection(projection);

// Add the canvas to the page
var svg = d3.select("div#map")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Color scale for the map
var colorscale = d3.scale.linear()
    .domain([-1.0, 0, 1.0])
    .range(["red", "white", "skyblue"]);

// Define tooltips
var tooltip = d3.select("body")
        .append("div")   
        .attr("class", "tooltip")               
        .style("opacity", 0);

// Color scale for the legend
var color = d3.scale.linear()
    .domain([0,1,2,3])
    .range(["gray", "red", "white", "skyblue"])

// Text for the legend
var legendText = ["Positive", "Neutral", "Negative", "No Data"];

// Load all the data into the map
d3.json("static/us-states.json", function(json) {
    d3.csv("static/map_data.csv?q="+Math.random(), function(dat) {
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

        // draw the states
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
            // highlight state and display the tooltip on mouseover
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
            // unhighlight state and make tooltip disappear on mouseout
            .on("mouseout", function(d) {
                d3.select(this)
                    .style("stroke", "#000")
                    .style("stroke-width", "1");

                tooltip.transition()        
                   .duration(500)      
                   .style("opacity", 0);
            });

        // Create map legend
        // Modified Legend Code from Mike Bostock: http://bl.ocks.org/mbostock/3888852
        var legend = d3.select("body").append("svg")
            .attr("class", "legend")
            .attr("width", 140)
            .attr("height", 200)
            .selectAll("g")
            .data(color.domain().slice().reverse())
            .enter()
            .append("g")
            .attr("transform", function(d, i) { return "translate(0," + i * 25 + ")"; });

        legend.append("rect")
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", color)
            .style("stroke", "black")
            .style("stroke-width", "0.5");

        legend.append("text")
            .data(legendText)
            .attr("x", 24)
            .attr("y", 9)
            .attr("dy", ".35em")
            .text(function(d) { return d; });
    })
});
