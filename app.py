from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

# Automatically make the year available in all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username:
            session['user'] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Please enter a username.")
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            session['user'] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("register.html", register_error="Please enter a valid username and password.")
    return render_template("register.html")

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    user = session.get("user", "Guest")
    salary = None
    breakdown = None
    remaining = None
    savings_goal = None
    monthly_save = None

    if request.method == "POST":
        form_type = request.form.get("form_type")

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
        answers = {
            "q1": request.form.get("q1"),
            "q2": request.form.get("q2"),
            "q3": request.form.get("q3"),
            "q4": request.form.get("q4"),
            "q5": request.form.get("q5"),
            "q6": request.form.get("q6"),
            "q7": request.form.get("q7"),
            "q8": request.form.get("q8"),
            "q9": request.form.get("q9"),
            "q10": request.form.get("q10"),
            "status": request.form.get("status"),
        }

        # Analyze preference (q1–q5)
        preference_score = sum(1 for q in ["q1", "q2", "q3", "q4", "q5"] if answers[q] == "expensive")

        # Analyze discipline (q6–q10)
        discipline_score = sum(1 for q in ["q6", "q7", "q8", "q9", "q10"] if answers[q] == "disciplined")

        status = answers["status"]

        # Decision logic
        if preference_score >= 4 and discipline_score <= 1 and status == "struggling":
            message = "You may be living above your means. Try budgeting and cutting back on non-essentials."
        elif preference_score >= 3 and status in ["struggling", "okay"]:
            message = "Consider balancing your lifestyle with your income to improve financial health."
        elif discipline_score >= 4 and status == "great":
            message = "You're managing your money well! Keep it up!"
        elif discipline_score >= 3 and preference_score <= 2 and status == "okay":
            message = "You're on the right track. A little more discipline could go a long way."
        else:
            message = "Consider reflecting on your habits and building a savings plan for better security."

        return render_template("quiz_result.html", message=message)

    return render_template("quiz.html")

if __name__ == '__main__':
    app.run(debug=True)