# ==============================
# Main Disc Tracker App
# by Stephanie Huang
# May 2014
# Using Flask
# ==============================

from flask import Flask, render_template, request
import file_writer, grapher, os

app = Flask(__name__)

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        date = request.form['year'] + "-" + request.form['month'] + "-" \
            + request.form['day']
        name = request.form['name']
        minutes = request.form['minutes']

        file_writer.readWrite(date, name, minutes)
        return render_template("posted.html")
    else:
        return render_template("form.html")

@app.route("/graph")
def graph():
    grapher.graph()
    return render_template("graph.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server(error):
    return render_template("500.html"), 500

#port = int(os.environ.get("PORT", 5000))
#app.run(host="0.0.0.0", port=port)
app.run(debug=True)