# Jorge Daniel Gómez Quintana "Finance"

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
    rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = rows[0]["cash"]

    # Get user's portfolio
    portfolio = db.execute(
        "SELECT symbol, shares FROM portfolio WHERE user_id = ?", session["user_id"])

    stocks = []
    total_value = 0

    for stock in portfolio:
        symbol = stock["symbol"]
        shares = stock["shares"]
        quote = lookup(symbol)
        if quote:
            price = quote["price"]
            total = price * shares
            total_value += total
            stocks.append({
                "symbol": symbol,
                "name": quote["name"],
                "shares": shares,
                "price": price,
                "total": total
            })

    grand_total = cash + total_value

    return render_template("index.html", stocks=stocks, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Validate symbol
        if not symbol:
            return apology("must provide symbol", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)

        # Validate shares
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be positive integer", 400)
        except ValueError:
            return apology("shares must be integer", 400)

        # Calculate total cost
        total_cost = shares * stock["price"]

        # Check user's cash
        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"]

        if total_cost > cash:
            return apology("can't afford", 400)

        # Update cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])

        # Record transaction
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
        """, session["user_id"], symbol, shares, stock["price"])

        # Update portfolio
        current_shares = db.execute("""
            SELECT shares FROM portfolio
            WHERE user_id = ? AND symbol = ?
        """, session["user_id"], symbol)

        if current_shares:
            new_shares = current_shares[0]["shares"] + shares
            db.execute("""
                UPDATE portfolio SET shares = ?
                WHERE user_id = ? AND symbol = ?
            """, new_shares, session["user_id"], symbol)
        else:
            db.execute("""
                INSERT INTO portfolio (user_id, symbol, shares)
                VALUES (?, ?, ?)
            """, session["user_id"], symbol, shares)

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("""
        SELECT symbol, shares, price, transacted
        FROM transactions
        WHERE user_id = ?
        ORDER BY transacted DESC
    """, session["user_id"])

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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
            return apology("must provide symbol", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate inputs
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if not confirmation:
            return apology("must confirm password", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        # Hash password
        hash = generate_password_hash(password)

        # Insert new user
        try:
            new_user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("username already exists", 400)

        # Log user in
        session["user_id"] = new_user_id
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate inputs
        if not symbol:
            return apology("must select symbol", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be positive integer", 400)
        except ValueError:
            return apology("shares must be integer", 400)

        # Check available shares
        stock = db.execute("""
            SELECT shares FROM portfolio
            WHERE user_id = ? AND symbol = ?
        """, session["user_id"], symbol)

        if not stock or stock[0]["shares"] < shares:
            return apology("not enough shares", 400)

        # Get current price
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        total_sale = shares * quote["price"]

        # Update user cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale, session["user_id"])

        # Record transaction
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
        """, session["user_id"], symbol, -shares, quote["price"])

        # Update portfolio
        new_shares = stock[0]["shares"] - shares
        if new_shares == 0:
            db.execute("DELETE FROM portfolio WHERE user_id = ? AND symbol = ?",
                       session["user_id"], symbol)
        else:
            db.execute("""
                UPDATE portfolio SET shares = ?
                WHERE user_id = ? AND symbol = ?
            """, new_shares, session["user_id"], symbol)

        flash("Sold!")
        return redirect("/")

    else:
        # Get user's stocks for dropdown
        stocks = db.execute("""
            SELECT symbol FROM portfolio
            WHERE user_id = ?
        """, session["user_id"])
        return render_template("sell.html", stocks=stocks)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add additional cash to account"""
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            if amount <= 0:
                return apology("amount must be positive", 400)
        except ValueError:
            return apology("invalid amount", 400)

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])
        flash(f"Added ${amount:,.2f} to your account!")
        return redirect("/")

    else:
        return render_template("add_cash.html")
