from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(db.String(200))

    role = db.Column(db.String(50))

class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    description = db.Column(db.String(200))

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    assigned_to = db.Column(db.String(100))

    due_date = db.Column(db.String(50))

    status = db.Column(db.String(50))