from flask import Flask, render_template, request, redirect, session
from models import db, User, Project, Task
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        existing_user = User.query.filter_by(
            email=request.form['email']
        ).first()

        if existing_user:
            return "Email already exists"

        hashed_password = bcrypt.generate_password_hash(
            request.form['password']
        ).decode('utf-8')

        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=hashed_password,
            role=request.form['role']
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = User.query.filter_by(
            email=request.form['email']
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            request.form['password']
        ):

            session['user'] = user.email

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/create_project", methods=["GET", "POST"])
def create_project():

    if request.method == "POST":

        project = Project(
            title=request.form['title'],
            description=request.form['description']
        )

        db.session.add(project)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("create_project.html")

@app.route("/create_task", methods=["GET", "POST"])
def create_task():

    if request.method == "POST":

        task = Task(
            title=request.form['title'],
            assigned_to=request.form['assigned_to'],
            due_date=request.form['due_date'],
            status=request.form['status']
        )

        db.session.add(task)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("create_task.html")

@app.route("/tasks")
def tasks():

    all_tasks = Task.query.all()

    return render_template(
        "tasks.html",
        tasks=all_tasks
    )

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        user = User.query.filter_by(
            email=request.form['email']
        ).first()

        if user:

            user.password = bcrypt.generate_password_hash(
                request.form['new_password']
            ).decode('utf-8')

            db.session.commit()

            return redirect("/login")

        return "User not found"

    return render_template("forgot_password.html")

@app.route("/logout")
def logout():

    session.pop('user', None)

    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)