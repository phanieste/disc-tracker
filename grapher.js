/* Attempt 2 */

var margin = {'top': 20, 'bottom': 20, 'left': 20, 'right': 20},
    width = 1000,
    height = 400;

var svgWrapper = d3.select('body')
    .append('svg')
    .attr('height', height)
    .attr('width', width);

// setting up colors for each line in graph
var colorRange = colorbrewer.Spectral[11].concat(colorbrewer.RdPu[9], 
    colorbrewer.PuBu[9]);
var color = d3.scale.ordinal()
var newColors = function (colors, numColors) {
    var newRange = [];
    for (i = 0; i < numColors; i++) {
        newRange[i] = colors[i];
    }
    return newRange;
}

// set up scales for x and y axes
var x = d3.scale.linear();
    x.rangeRound([0, width]);
var y = d3.scale.linear();
    y.rangeRound([0, height]);

// get minutes value
var getMinutes = function (d, player) {
    var index = d3.keys(d).indexOf(player);
    return parseInt(d3.values(d)[index]);
}

// parse data
d3.tsv('data.tsv', function (error, data) {
    var xAxisVar = 'date';

    var players = d3.keys(data[0])
        .filter(function (key) {
            return key !== xAxisVar;
        });

    var dayOne = data[0].date;

    // defining domain & range for colors
    color.domain(players);
    var playerColors = newColors(colorRange, players.length);
    color.range(playerColors);

    var timeData = players.map(function (player) {
        return {
            'name': player,
            'disc_time': data.map(function (d) {
                return {
                    'name': player,
                    'day': parseInt(d.date)-dayOne,
                    'minutes': getMinutes(d, player)
                };
            })
        };
    })

    // set domain for scaling x and y axes
    x.domain(d3.extent(data, function (d) { return parseInt(d.date)-dayOne; }));
    y.domain([0, 
        d3.max(timeData, function (d) {
            return d3.max(d.disc_time, function(c) {
                return c.minutes;
            });
        })
    ]);

    // line path function
    var line = d3.svg.line()
        .x(function (d) { return x(d.day); })
        .y(function (d) { return height-y(d.minutes); })
        .interpolate('linear');

    // draw paths on graph
    var lines = svgWrapper.selectAll('.lines')
        .data(timeData)
        .enter()
        .append('g')
        .attr('class', 'lines');

    lines.append('path')
        .attr('class', 'line')
        .attr('d', function (d) { return line(d.disc_time); })
        .attr('stroke', function (d) { return color(d.name); })
        .attr('stroke-width', 2)
        .style('fill', 'none');

})

