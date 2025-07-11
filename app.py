from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy database for users
users = {
    "johndoe123": "securepass456"
}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")

        if username in users and users[username] == password:
            return redirect(url_for("dashboard", user=username))
        else:
            return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users:
            return render_template("register.html", register_error="Username already exists.")
        users[username] = password
        return redirect(url_for("login"))
    return render_template("register.html")

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
