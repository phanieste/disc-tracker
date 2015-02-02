/*********************
 * Grapher using D3
*********************/

var grapher = function(data) {
    // Set up data and processing
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

    var sums = [], sum = 0;
    for (var i = 0, n = vals.length; i < n; i++) {
        for (var j = 0, m = vals[i].length; j < m; j++) {
            sum += vals[i][j].minutes;
        }
        sums.push(sum);
        sum = 0;        
    }
    console.log(sums);

    // Set up measurements
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        barHeight = 20,
        width = 800 - margin.left - margin.right,
        height = (barHeight+5) * entries.length;
    
    // Set scales
    var x = d3.scale.linear().range([0, width])
        .domain([0, d3.max(sums)]);
    var y = d3.scale.ordinal().domain(d3.keys(data))
        .rangeRoundBands([height, 0]);
    var colors = d3.scale.category10().domain(d3.keys(data));
    var timeScale = d3.time.scale().range([0, width-20])
        .domain(d3.extent(dates));

    // Set axes
    var xAxis = d3.svg.axis().scale(x).orient("bottom");
    var yAxis = d3.svg.axis().scale(y).orient("left");

    // Set up canvas
    var barChart = d3.select("#bar-graph")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left 
                + "," + margin.top + ")");

    // line graphs
    // var line = d3.svg.line()
    //     .x(function(d) { 
    //         // console.log(x(parseDate(d.date))); //test
    //         return xl(parseDate(d.date)); })
    //     .y(function(d) { 
    //         // console.log(y(+d.minutes)); // test
    //         return yl(d.minutes); })
    //     .interpolate("linear");

    // lineChart.selectAll(".line")
    //     .data(entries)
    // .enter().append("path")
    //     .attr("class", "line")
    //     .attr("d", function (d) { 
    //         // console.log(d);
    //         return line(d.value); })
    //     .attr("fill", "none")
    //     .attr("stroke", function (d) { return colors(d.key); })
    //     .attr("stroke-width", 2);

    // bar graph
    barChart.selectAll(".bar")
        .data(entries)
    .enter().append("rect")
        .attr("class", "bar")
        .attr("width", function (d) {
            var total = 0;
            for (var i = 0, n = d.value.length; i < n; i++) {
                total += d.value[i].minutes;
            }
            return x(total);
        })
        .attr("height", barHeight)
        .attr("x", 0)
        .attr("y", function(d) { return y(d.key); })
        .attr("fill", function (d) { return colors(d.key); });

    // attach axes
    // lineChart.append("g")
    //     .attr("class", "x axis")
    //     .attr("transform", "translate(0," + height + ")")
    //     .call(xAxisL);
    // lineChart.append("g")
    //     .attr("class", "y axis")
    //     .call(yAxisL);

};

// execute graphing
grapher(window.data);