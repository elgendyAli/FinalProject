from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login():
    name = request.form.get("name")
    if name:
        return redirect(url_for("dashboard", user=name))
    return render_template("login.html", error="Please enter a name.")

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    user = request.args.get("user", "Guest")
    salary = None
    expenses = None
    savings_goal = None
    monthly_save = None

    if request.method == "POST":
        if request.form.get("salary"):
            try:
                salary = float(request.form.get("salary"))
                expenses = {
                    "rent": round(salary * 0.30, 2),
                    "groceries": round(salary * 0.15, 2),
                    "personal": round(salary * 0.10, 2),
                    "loan": round(salary * 0.20, 2),
                    "other": round(salary * 0.05, 2),
                }
                expenses["remaining"] = round(salary - sum(expenses.values()), 2)
            except:
                pass

        if request.form.get("goal_amount") and request.form.get("goal_months"):
            try:
                amount = float(request.form.get("goal_amount"))
                months = int(request.form.get("goal_months"))
                savings_goal = amount
                monthly_save = round(amount / months, 2)
            except:
                pass

    return render_template(
        "dashboard.html",
        user=user,
        salary=salary,
        expenses=expenses,
        savings_goal=savings_goal,
        monthly_save=monthly_save
    )

if __name__ == '__main__':
    app.run(debug=True)
