from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -----------------------------
# Database Models
# -----------------------------
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# -----------------------------
# HTML Template
# -----------------------------
TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Budget Tracker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 80%; margin-bottom: 20px; }
        th, td { border: 1px solid black; padding: 8px; text-align: center; }
        th { background-color: #f2f2f2; }
        form { margin-bottom: 20px; }
        input { margin-right: 10px; }
        h2 { margin-top: 40px; }
    </style>
</head>
<body>
    <h1>💰 Budget Tracker</h1>

    <!-- Add Income -->
    <h2>Add Income</h2>
    <form method="POST" action="{{ url_for('add_income') }}">
        <input type="text" name="source" placeholder="Source" required>
        <input type="number" step="0.01" name="amount" placeholder="Amount" required>
        <button type="submit">Add Income</button>
    </form>

    <h3>All Income</h3>
    <table>
        <tr><th>ID</th><th>Source</th><th>Amount</th><th>Date</th><th>Actions</th></tr>
        {% for inc in incomes %}
        <tr>
            <td>{{ inc.id }}</td>
            <td>{{ inc.source }}</td>
            <td>{{ inc.amount }}</td>
            <td>{{ inc.date.strftime('%Y-%m-%d %H:%M') }}</td>
            <td>
                <a href="{{ url_for('edit_income', income_id=inc.id) }}">Edit</a> |
                <a href="{{ url_for('delete_income', income_id=inc.id) }}" onclick="return confirm('Delete this income?')">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>

    <!-- Add Expense -->
    <h2>Add Expense</h2>
    <form method="POST" action="{{ url_for('add_expense') }}">
        <input type="text" name="category" placeholder="Category" required>
        <input type="number" step="0.01" name="amount" placeholder="Amount" required>
        <input type="text" name="description" placeholder="Description">
        <button type="submit">Add Expense</button>
    </form>

    <!-- Filter Expenses by Category -->
    <form method="GET" action="{{ url_for('index') }}">
        <input type="text" name="filter_category" placeholder="Filter by Category" value="{{ filter_category }}">
        <button type="submit">Filter</button>
        <a href="{{ url_for('index') }}">Reset</a>
    </form>

    <h3>All Expenses</h3>
    <table>
        <tr><th>ID</th><th>Category</th><th>Amount</th><th>Description</th><th>Date</th><th>Actions</th></tr>
        {% for exp in expenses %}
        <tr>
            <td>{{ exp.id }}</td>
            <td>{{ exp.category }}</td>
            <td>{{ exp.amount }}</td>
            <td>{{ exp.description }}</td>
            <td>{{ exp.date.strftime('%Y-%m-%d %H:%M') }}</td>
            <td>
                <a href="{{ url_for('edit_expense', expense_id=exp.id) }}">Edit</a> |
                <a href="{{ url_for('delete_expense', expense_id=exp.id) }}" onclick="return confirm('Delete this expense?')">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>

    <h2>Summary</h2>
    <p><strong>Total Income:</strong> {{ total_income }}</p>
    <p><strong>Total Expenses:</strong> {{ total_expense }}</p>
    <p><strong>Remaining Balance:</strong> {{ total_income - total_expense }}</p>

</body>
</html>
"""

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    filter_category = request.args.get('filter_category', '')
    
    # Expenses
    exp_query = Expense.query
    if filter_category:
        exp_query = exp_query.filter(Expense.category.ilike(f"%{filter_category}%"))
    expenses = exp_query.order_by(Expense.date.desc()).all()
    total_expense = sum(exp.amount for exp in expenses)

    # Income
    incomes = Income.query.order_by(Income.date.desc()).all()
    total_income = sum(inc.amount for inc in incomes)

    return render_template_string(TEMPLATE, expenses=expenses, incomes=incomes,
                                  total_expense=total_expense, total_income=total_income,
                                  filter_category=filter_category)

# -----------------------------
# Expense Routes
# -----------------------------
@app.route("/add", methods=["POST"])
def add_expense():
    category = request.form['category']
    amount = float(request.form['amount'])
    description = request.form.get('description', '')
    new_expense = Expense(category=category, amount=amount, description=description)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    exp = Expense.query.get_or_404(expense_id)
    db.session.delete(exp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    exp = Expense.query.get_or_404(expense_id)
    if request.method == "POST":
        exp.category = request.form['category']
        exp.amount = float(request.form['amount'])
        exp.description = request.form.get('description', '')
        db.session.commit()
        return redirect(url_for('index'))
    edit_template = """
    <h2>Edit Expense</h2>
    <form method="POST">
        <input type="text" name="category" value="{{ expense.category }}" required>
        <input type="number" step="0.01" name="amount" value="{{ expense.amount }}" required>
        <input type="text" name="description" value="{{ expense.description }}">
        <button type="submit">Update</button>
    </form>
    <a href="{{ url_for('index') }}">Back</a>
    """
    return render_template_string(edit_template, expense=exp)

# -----------------------------
# Income Routes
# -----------------------------
@app.route("/add_income", methods=["POST"])
def add_income():
    source = request.form['source']
    amount = float(request.form['amount'])
    new_income = Income(source=source, amount=amount)
    db.session.add(new_income)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete_income/<int:income_id>")
def delete_income(income_id):
    inc = Income.query.get_or_404(income_id)
    db.session.delete(inc)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/edit_income/<int:income_id>", methods=["GET", "POST"])
def edit_income(income_id):
    inc = Income.query.get_or_404(income_id)
    if request.method == "POST":
        inc.source = request.form['source']
        inc.amount = float(request.form['amount'])
        db.session.commit()
        return redirect(url_for('index'))
    edit_template = """
    <h2>Edit Income</h2>
    <form method="POST">
        <input type="text" name="source" value="{{ income.source }}" required>
        <input type="number" step="0.01" name="amount" value="{{ income.amount }}" required>
        <button type="submit">Update</button>
    </form>
    <a href="{{ url_for('index') }}">Back</a>
    """
    return render_template_string(edit_template, income=inc)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)