import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Query user's holdings and cash
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    holdings = {}
    for transaction in transactions:
        symbol = transaction["symbol"]
        shares = transaction["shares"]
        if symbol in holdings:
            holdings[symbol]["shares"] += shares
        else:
            holdings[symbol] = {
                "shares": shares,
                "price": lookup(symbol)["price"]
            }
    total_value = sum(stock["shares"] * stock["price"] for stock in holdings.values())
    grand_total = total_value + cash

    return render_template("index.html", holdings=holdings, cash=cash, total_value=total_value, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol and shares were submitted
        if not symbol or not shares:
            return apology("must provide symbol and shares", 400)

        shares = int(shares)

        # Ensure a positive integer for shares
        if shares < 1:
            return apology("shares must be a positive integer", 400)

        quote = lookup(symbol)

        # Ensure the symbol is valid
        if quote is None:
            return apology("invalid symbol", 400)

        # Calculate total cost
        cost = shares * quote["price"]

        # Query user's cash balance
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Ensure user can afford
        if cash < cost:
            return apology("can't afford", 400)

        # Update the user's cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])

        # Store the transaction
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, shares, quote["price"])

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Query user's transactions
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Query the API (or function) for the stock symbol
        quote = lookup(symbol)

        # Ensure the symbol is valid
        if quote is None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # TODO: Validate form input
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("Must provide username and password", 403)
        elif password != confirmation:
            return apology("Passwords must match", 403)

        # TODO: Check if username exists
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            return apology("Username already exists", 403)

        # TODO: Insert new user into database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        # Log the user in
        session["user_id"] = new_user_id

        # Redirect user to home page
        return redirect("/")

        # TODO: Log user in and redirect to home page
        pass
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate inputs
        if not symbol or not shares.isnumeric() or int(shares) < 1:
            return apology("Invalid symbol and/or shares", 400)

        # Ensure user owns enough of the stock
        owned_shares = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?",
                                  session["user_id"], symbol)[0]["total_shares"]

        if owned_shares is None or int(shares) > owned_shares:
            return apology("Not enough shares", 400)

        # Update user cash
        quote = lookup(symbol)
        earnings = quote["price"] * int(shares)
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", earnings, session["user_id"])

        # Log the sale (negative shares)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, -int(shares), quote["price"])

        # Redirect to home page
        return redirect("/")
    else:
        # Query symbols for dropdown
        symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", session["user_id"])
        symbols = [symbol["symbol"] for symbol in symbols]
        return render_template("sell.html", symbols=symbols)

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "POST":
        # Ensure amount is positive number
        amount = request.form.get("amount")
        if not amount or not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            return apology("Invalid amount", 400)

        # Update user cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", float(amount), session["user_id"])

        # Redirect to home page
        return redirect("/")
    else:
        return render_template("add_cash.html")