/*********************
 * Grapher using D3
*********************/

var grapher = function(data) {
    // set up
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 800 - margin.left - margin.right;
        height = 400 - margin.top - margin.bottom;

    // console.log(data);
    var entries = d3.entries(data);
    // console.log(entries); // test
    var parseDate = d3.time.format("%Y-%m-%dT%X.%L%L%L%Z")
        .parse;

    // Collect all dates
    var vals = d3.values(data)[0];
    var dates = [];
    for (var i = 0, n = vals.length; i < n; i++) {
        dates.push(parseDate(vals[i].date));
        // console.log(parseDate(vals[i].date)); // test
    }
    // console.log(dates); // test

    // Collect all minutes
    vals = d3.values(data);
    var mins = [];
        // loop through each column
    for (var i = 0, n = vals.length; i < n; i++) {
            // loop through each element in columns
        for (var j = 0, m = vals[i].length; j < m; j++) {
            mins.push(vals[i][j].minutes);
        }
    }
    // console.log(mins); // test
    
    // Set scales
    var xl = d3.time.scale().range([0, width-20])
        .domain(d3.extent(dates));
    var yl = d3.scale.linear().range([height-5, 0])
        .domain(d3.extent(mins));
    var colors = d3.scale.category10().domain(d3.keys(data));

    // Set axes
    var xAxisL = d3.svg.axis().scale(xl).orient("bottom");
    var yAxisL = d3.svg.axis().scale(yl).orient("left");

    // set up canvas
    var lineChart = d3.select("#line-graph")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" 
                + margin.left + "," + margin.top + ")");

    var barChart = d3.select("#bar-graph")
        .append("svg");

    // line graphs
    var line = d3.svg.line()
        .x(function(d) { 
            // console.log(x(parseDate(d.date))); //test
            return xl(parseDate(d.date)); })
        .y(function(d) { 
            // console.log(y(+d.minutes)); // test
            return yl(d.minutes); })
        .interpolate("linear");

    lineChart.selectAll(".line")
        .data(entries)
    .enter().append("path")
        .attr("class", "line")
        .attr("d", function (d) { 
            // console.log(d);
            return line(d.value); })
        .attr("fill", "none")
        .attr("stroke", function (d) { return colors(d.key); })
        .attr("stroke-width", 2);

    // bar graph

    // attach axes
    lineChart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxisL);
    lineChart.append("g")
        .attr("class", "y axis")
        .call(yAxisL);

};

// execute graphing
grapher(window.data);