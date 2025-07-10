from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy credentials
USERNAME = "johndoe123"
PASSWORD = "securepass456"

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == USERNAME and password == PASSWORD:
        return redirect(url_for("dashboard"))
    return render_template("login.html", error="Invalid username or password.")

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    expenses = None
    salary = None

    if request.method == "POST":
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

    return render_template("dashboard.html", salary=salary, expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)
