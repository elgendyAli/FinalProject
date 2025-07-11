from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username:
            return redirect(url_for("dashboard", user=username))
        return render_template("login.html", error="Please enter a username.")
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # 🔐 Optional: save this to a database or file later
        if username and password:
            return redirect(url_for("dashboard", user=username))
        else:
            return render_template("register.html", register_error="Please enter a valid username and password.")
    return render_template("register.html")

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    user = request.args.get("user", "Guest")
    salary = None
    breakdown = None
    remaining = None
    savings_goal = None
    monthly_save = None

    if request.method == "POST":
        form_type = request.form.get("form_type")

        # Budget planner
        if form_type == "budget":
            try:
                salary = float(request.form.get("salary"))
                breakdown = []
                total_spent = 0

                for i in range(1, 6):
                    name = request.form.get(f"cat_name_{i}")
                    amount = request.form.get(f"cat_amount_{i}")
                    percent = request.form.get(f"cat_percent_{i}")

                    if name:
                        if amount:
                            value = round(float(amount), 2)
                        elif percent:
                            value = round((float(percent) / 100) * salary, 2)
                        else:
                            continue

                        total_spent += value
                        breakdown.append({"name": name, "amount": value})

                remaining = round(salary - total_spent, 2)
            except ValueError:
                pass

        # Savings planner
        elif form_type == "savings":
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
        breakdown=breakdown,
        remaining=remaining,
        savings_goal=savings_goal,
        monthly_save=monthly_save
    )

if __name__ == '__main__':
    app.run(debug=True)