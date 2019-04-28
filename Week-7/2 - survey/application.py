import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # Get POST parameters
    name = request.form.get('name')
    house = request.form.get('house')
    position = request.form.get('position')
    # Validate POST parameters
    if not name:
        return render_template("error.html", message="name was not specified")
    if not house:
        return render_template("error.html", message="great house was not specified")
    if not position:
        return render_template("error.html", message="position was not specified")
    # Insert row in survey.csv
    fields = [name, house, position]
    with open("survey.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    data = []
    # read csv and pass data to client
    with open("survey.csv", "r") as f:
        reader = csv.reader(f)
        for d in reader:
            data.append(d)
    return render_template("sheet.html", data=data)
