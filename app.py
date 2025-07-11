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

@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        # Preference: expensive = +2, moderate = +1, affordable = 0
        # Habits: disciplined = 0, moderate = +1, risky = +2
        # Financial status: great = 0, okay = +1, struggling = +2

        score = 0

        preference_questions = ['q1', 'q2', 'q3', 'q4', 'q5']
        habit_questions = ['q6', 'q7', 'q8', 'q9', 'q10']
        status = request.form.get("status")

        for q in preference_questions:
            val = request.form.get(q)
            if val == "expensive":
                score += 2
            elif val == "moderate":
                score += 1

        for q in habit_questions:
            val = request.form.get(q)
            if val == "risky":
                score += 2
            elif val == "moderate":
                score += 1

        if status == "okay":
            score += 1
        elif status == "struggling":
            score += 2

        # Interpretation based on score (max is 22, min is 0)
        if score <= 5:
            advice = "You’re on track financially! Your preferences and habits align well with responsible spending."
        elif score <= 10:
            advice = "You're doing okay, but keep an eye on your spending preferences and try to plan ahead more often."
        elif score <= 16:
            advice = "You're at risk of overspending. Consider adjusting your preferences and improving your money habits."
        else:
            advice = "Your current lifestyle may not be financially sustainable. Try creating a tighter budget and reducing luxury purchases."

        return render_template("quiz_result.html", advice=advice)

    return render_template("quiz.html")

if __name__ == '__main__':
    app.run(debug=True)