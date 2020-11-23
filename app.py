import sqlite3

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


''''# Configure session to use filesystem (instead of signed cookies)
app.secret_key = "BC7D5D5AEC563ECBC74ED896427363E95E87781F51FAB8095128F192423A98D4"
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"'''


@app.route("/")
def index():
    """index"""
    year = "2020"
    # connect database to sqlite
    db = sqlite3.connect("movies.db")

    cursor = db.execute("SELECT * "
                        "FROM movieMaster "
                        "WHERE startYear == ? "
                        "ORDER BY "
                        "rating DESC LIMIT 10", (year,))

    # render results page
    return render_template("index.html", year=year, items=cursor)

@app.route("/result", methods=["GET", "POST"])
def result():
    """Display results"""

    if request.method == "POST":

        # connect database to sqlite
        db = sqlite3.connect("movies.db")

        # year from user from index.html
        year = request.form.get("year")
        int_year = int(year)

        # check user entered a valid year
        if 1916 <= int_year <= 2020:

            cursor = db.execute("SELECT * "
                                "FROM movieMaster "
                                "WHERE startYear == ? "
                                "ORDER BY "
                                "rating DESC LIMIT 10", (year,))

            # render results page
            return render_template("results.html", year=year, items=cursor)

        # user entered an invalid year
        else:
            message = "Please enter a year between 1916 and 2020."
            return render_template("index.html", message=message)



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return (e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
