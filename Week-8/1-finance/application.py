import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute(
        "SELECT id, user_id, symbol, SUM(shares) shares, price  FROM history WHERE user_id = :id GROUP BY symbol", id=session["user_id"])
    data = []
    total_grand = 0
    for r in rows:
        quote = lookup(r['symbol'])
        com_name = "unknown"
        if quote:
            com_name = quote['name']
        total = float(r['price'])*float(r['shares'])
        total_grand += total
        data.append([r['symbol'], com_name, r['shares'], usd(r['price']), usd(total)])
    # Get current cash
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]['cash']
    total_grand += cash
    return render_template("index.html", data=data, cash=usd(cash), total=usd(total_grand))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol", 400)
        quote = lookup(symbol)
        if not quote:
            return apology("quote not found", 400)
        shares = request.form.get("shares")
        if not shares:
            return apology("missing shares", 400)
        # Validate shares
        try:
            int(shares)
        except ValueError:
            return apology("shares must be integer", 400)
        if int(shares) <= 0:
            return apology("shares must be positive integer", 400)
        # Ensure user has enough money
        cash = db.execute("SELECT cash FROM users WHERE id = :id",
                          id=session["user_id"])[0]['cash']
        price = quote['price']
        if cash < price * int(shares):
            return apology("not enough cash", 400)
        # Insert history record
        db.execute("INSERT INTO history(user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=symbol, shares=shares, price=price)
        # Subtract total price from user's cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", id=session["user_id"], cash=cash-price * int(shares))
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    if not username:
        return jsonify(False)
    user = db.execute("SELECT * FROM users WHERE username = :username", username=username)
    # Ensure there is no such user
    if user:
        return jsonify(False)
    return jsonify(True)


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Add cash to user account"""
    if request.method == "POST":
        deposit = request.form.get("deposit")
        if not deposit:
            return apology("missing deposit", 400)
        if isinstance(deposit, float):
            return apology("deposit must be positive integer", 400)
        if isinstance(deposit, int) and int(deposit) <= 0:
            return apology("deposit must be positive integer", 400)
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]['cash']
        # Add money to user cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", id=session["user_id"], cash=cash + int(deposit))
        return redirect("/")
    else:
        return render_template("deposit.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM history WHERE user_id = :id", id=session["user_id"])
    data = []
    total_grand = 0
    for r in rows:
        data.append([r['symbol'], r['shares'], usd(r['price']), r['transaction_date']])
    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol", 400)
        quote = lookup(symbol)
        if not quote:
            return apology("quote not found", 400)
        quote['price'] = usd(quote['price'])
        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)
        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        # Ensure there is no such user
        if user:
            return apology("username already exists", 400)
        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)
        # Ensure password was confirmed
        if not confirmation:
            return apology("must provide password confirmation", 400)
        # Ensure passwords match
        if password != confirmation:
            return apology("passwords do not match", 400)
        # Insert user record to db
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)", username=username, hash=hash)
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol", 400)
        quote = lookup(symbol)
        if not quote:
            return apology("quote not found", 400)
        sell_count = request.form.get("shares")
        if not sell_count:
            return apology("amount of selling stocks not defined", 400)
        sell_count = int(sell_count)
        if isinstance(sell_count, float):
            return apology("amount of selling stocks must be positive integer", 400)
        if isinstance(sell_count, int) and sell_count <= 0:
            return apology("amount of selling stocks must be positive integer", 400)
        rows = db.execute("SELECT * FROM history WHERE user_id = :id AND symbol=:symbol", id=session["user_id"], symbol=symbol)
        total_stocks = 0
        for r in rows:
            total_stocks += int(r['shares'])
        if sell_count > total_stocks:
            return apology("shares capacity exceeded", 400)
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]['cash']
        price = quote['price']
        # Insert history record
        db.execute("INSERT INTO history(user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=symbol, shares=-sell_count, price=price)
        # Add total price to user's cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", id=session["user_id"], cash=cash+price * int(sell_count))
        return redirect("/")
    else:
        rows = db.execute("SELECT DISTINCT symbol FROM history WHERE user_id = :id", id=session["user_id"])
        data = []
        for r in rows:
            data.append(r['symbol'])
        return render_template("sell.html", data=data)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
