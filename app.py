# ==============================
# Main Disc Tracker App
# by Stephanie Huang
# May 2014
# Using Flask
# ==============================

from flask import Flask, render_template, request
import file_writer, grapher

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
    return render_template("graphed.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run()
