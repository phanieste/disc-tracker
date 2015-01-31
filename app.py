# ==============================
# Main Disc Tracker App
# by Stephanie Huang
# May 2014
# Using Flask
# ==============================

from flask import Flask, render_template, request
from hashlib import sha1
import file_writer, grapher, os, boto
from boto.s3.key import Key

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

        # write file to S3 using boto
        S3_BUCKET = 'disc-tracker-assets'

        conn = boto.connect_s3()
        bucket = conn.get_bucket(S3_BUCKET, validate=False)

        file_writer.readWrite(date, name, minutes)

        k = Key(bucket)
        k.key = 'data.csv'
        k.set_contents_from_filename('temp.csv.tmp')
        k.make_public()

        return render_template("posted.html")
    else:
        return render_template("form.html")

@app.route("/graph")
def graph():
    return render_template("graph.html", data=d3grapher.graph())

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server(error):
    return render_template("500.html"), 500

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

# for testing on local server:
#app.run(debug=True)