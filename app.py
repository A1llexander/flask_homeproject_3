# -*- coding: utf-8 -*-

import random
from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route('/')
def render_main():
    with open("teachers.txt", "r") as f:
        teachers = json.load(f)
    output = render_template('index.html', teachers=random.sample(teachers, 6))
    return output


@app.route('/goals/<goal>/')
def render_goals(goal):
    with open("teachers.txt", "r") as f:
        teachers = json.load(f)
    output = render_template('goal.html', goal=goal, teachers=teachers)
    return output


@app.route('/profiles/<int:id>/')
def render_profiles(id):
    with open("teachers.txt", "r") as f:
        teachers = json.load(f)
    output = render_template('profile.html', teacher=teachers[id])
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
    with open("request.txt", "r") as f:
        booking = json.load(f)
        booking.append({'name': name, 'phone': phone, 'goal': goal, 'time': time})
    with open("request.txt", "w") as f:
        json.dump(booking, f)
    return output


@app.route('/booking/<int:id>/<week_day>/<time>/')
def render_booking(id, week_day, time):
    with open("teachers.txt", "r") as f:
        teachers = json.load(f)
    output = render_template('booking.html', teacher=teachers[id], week_day=week_day, time=time)
    return output


@app.route('/booking_done/', methods=['POST'])
def render_booking_done():
    clientName = request.form.get("clientName")
    clientPhone = request.form.get("clientPhone")
    clientWeekday = request.form.get("clientWeekday")
    clientTime = request.form.get("clientTime")
    output = render_template('booking_done.html', clientname=clientName, clientphone=clientPhone,
                             clientweekday=clientWeekday, clienttime=clientTime)

    with open("booking.txt", "r") as f:
        booking = json.load(f)
        booking.append({'clientName': clientName, 'clientPhone': clientPhone,
                        'clientWeekday': clientWeekday, 'clientTime': clientTime})
    with open("booking.txt", "w") as f:
        json.dump(booking, f)

    return output


if __name__ == '__main__':
    app.run(debug=True)
