NYPD Disc-Tracker
=====

This web app is written for NYPD, Columbia University's women's ultimate frisbee team, to keep track of team disc time over the summer.

It will allow individual users to input their disc time each day, and also display a graph of all players and their daily disc times in comparison with their teammates.

This web app is written using Python Flask and the graphing aspect is handled by Bokeh using color specifications and designs developed by Cynthia Brewer (http://colorbrewer.org).

The deployed app can be found here: http://disc-tracker.herokuapp.com/

This was a rather quickly-developed, simple app and is no longer in use! It is more of a prototype--definitely plenty of room for improvement. Great way to start knowing Flask.

UPDATE 2015-01-30: Decided to dust off this app briefly and experiment with d3.js. No longer in use, but I figured I'd make the data visualization prettier by using d3.js to draw the graphs.

# Changelog

 * scrapped line graph
 * switch to interactive bar graph
 * working overall bar graph

2015-02-01
 * functional d3.js line graph

2015-01-30
 * updated to use d3.js