import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import data as data

app = Flask(__name__)
app.secret_key = "randomstring"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Teachers(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.String, nullable=False)
    free = db.Column(db.String, nullable=False)
    lessons = db.relationship("Lessons")

class Lessons(db.Model):
    __tablename__ = "lessons"
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    day = db.Column(db.String, nullable=False )
    time = db.Column(db.String, nullable=False)
    booked = db.Column(db.Boolean, nullable=False)

class Request(db.Model):
    __tablename__ = "request"
    id = db.Column(db.Integer, primary_key=True)
    times_per_week = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, nullable=False )
    user_phone = db.Column(db.Integer, nullable=False)
    goal = db.Column(db.String, nullable=False)

db.create_all()

with open("teachers.txt", "r") as f:
    teachers = json.load(f)

lesson_count = 1
for teacher in teachers:
    print(teacher['name'])
    new_teacher = Teachers(
        id=teacher['id'],
        name=teacher['name'],
        about=teacher['about'],
        rating=teacher['rating'],
        picture=teacher['picture'],
        price=teacher['price'],
        goals=' '.join(teacher['goals']),
        free=json.dumps(teacher['free']))
    print(f"ID is {new_teacher.id}") # Получаю ID is None
    db.session.add(new_teacher)
    for day in teacher['free']:
        for time in teacher['free'][day]:
            new_lesson = Lessons(
                id=lesson_count,
                teacher_id=teacher['id'],
                day=day,
                time=time,
                booked=teacher['free'][day][time])
            db.session.add(new_lesson)
            lesson_count = lesson_count+1

db.session.commit()