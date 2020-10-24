# -*- coding: utf-8 -*-

import random
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

app = Flask(__name__)
app.secret_key = "randomstring"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
    user_name = db.Column(db.String, nullable=False)
    user_phone = db.Column(db.Integer, nullable=False)

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
    new_teacher = Teachers(
    #    id=teacher['id'],
        name=teacher['name'],
        about=teacher['about'],
        rating=teacher['rating'],
        picture=teacher['picture'],
        price=teacher['price'],
        goals=' '.join(teacher['goals']),
        free=json.dumps(teacher['free']))
    db.session.add(new_teacher)
    print(teacher['name'])
    for day in teacher['free']:
        for time in teacher['free'][day]:
            new_lesson = Lessons(
           #     id=lesson_count,
                teacher_id=teacher['id'],
                day=day,
                time=time,
                booked=teacher['free'][day][time],
                user_name='empty',
                user_phone=0)
            db.session.add(new_lesson)
            lesson_count = lesson_count+1

db.session.commit()

@app.route('/')
def render_main():
    output = render_template('index.html', teachers=db.session.query(Teachers).slice(1, 6))
    return output


@app.route('/goals/<goal>/')
def render_goals(goal):
    goal = '%' + goal + '%'
    output = render_template('goal.html', teachers=db.session.query(Teachers).filter(Teachers.goals.like(goal)), goal=goal)
    return output


@app.route('/profiles/<int:id>/')
def render_profiles(id):
    teacher = db.session.query(Teachers).filter(Teachers.id == id).first()
    output = render_template('profile.html', teacher=teacher, schedule=json.loads(teacher.free))
    return output


@app.route('/request/')
def render_request():
    output = render_template('request.html')
    return output


@app.route('/request_done/', methods=['POST'])
def render_request_done():
    goal = request.form.get("goal")
    time = request.form.get("time")
    name = request.form.get("name")
    phone = request.form.get("phone")
    output = render_template('request_done.html', name=name, phone=phone, goal=goal, time=time)
    new_request = Request(
        times_per_week=time,
        user_name=name,
        user_phone=phone,
        goal=goal)
    db.session.add(new_request)
    db.session.commit()
    return output


@app.route('/booking/<int:id>/<week_day>/<time>/')
def render_booking(id, week_day, time):
    teacher = db.session.query(Teachers).filter(Teachers.id == id).first()
    output = render_template('booking.html', teacher=teachers, week_day=week_day, time=time)
    return output


@app.route('/booking_done/', methods=['POST'])
def render_booking_done():
    clientName = request.form.get("clientName")
    clientPhone = request.form.get("clientPhone")
    clientWeekday = request.form.get("clientWeekday")
    clientTime = request.form.get("clientTime")
    clientTeacher = request.form.get("clientTeacher")
    output = render_template('booking_done.html', clientname=clientName, clientphone=clientPhone,
                             clientweekday=clientWeekday, clienttime=clientTime)

    new_lesson = Lessons(
        teacher_id=clientTeacher,
        day=clientWeekday,
        time=clientTime,
        booked=True,
        user_name=clientName,
        user_phone=clientPhone
    )
    db.session.add(new_lesson)
    db.session.commit()
    return output


if __name__ == '__main__':
    app.run(debug=True)
