from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route("/")
def index():

    conn = sqlite3.connect("finance.db")
    c = conn.cursor()

    incomes = c.execute("SELECT * FROM income ORDER BY id DESC").fetchall()
    expenses = c.execute("SELECT * FROM expense ORDER BY id DESC").fetchall()

    total_income = c.execute("SELECT SUM(amount) FROM income").fetchone()[0]
    total_expense = c.execute("SELECT SUM(amount) FROM expense").fetchone()[0]

    conn.close()

    if total_income is None:
        total_income = 0

    if total_expense is None:
        total_expense = 0

    profit = total_income - total_expense

    # 生成图表
    labels = ['Income', 'Expense']
    values = [total_income, total_expense]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Finance Chart")
    plt.savefig("static/chart.png")
    plt.close()

    return render_template(
        "index.html",
        incomes=incomes,
        expenses=expenses,
        total_income=total_income,
        total_expense=total_expense,
        profit=profit
    )


@app.route("/add_income", methods=["GET", "POST"])
def add_income():

    if request.method == "POST":

        amount = request.form["amount"]
        note = request.form["note"]
        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect("finance.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO income (amount,date,note) VALUES (?,?,?)",
            (amount, date, note)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_income.html")


@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        amount = request.form["amount"]
        note = request.form["note"]
        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect("finance.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO expense (amount,date,note) VALUES (?,?,?)",
            (amount, date, note)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_expense.html")


@app.route("/delete_income/<int:id>")
def delete_income(id):

    conn = sqlite3.connect("finance.db")
    c = conn.cursor()

    c.execute("DELETE FROM income WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete_expense/<int:id>")
def delete_expense(id):

    conn = sqlite3.connect("finance.db")
    c = conn.cursor()

    c.execute("DELETE FROM expense WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=5000)
# render fix    