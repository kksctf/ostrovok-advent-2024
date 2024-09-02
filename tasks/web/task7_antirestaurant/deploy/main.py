#!/usr/bin/env python

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request, url_for

app = Flask("task7_antirestaurant",
            template_folder=Path(__file__).parent / "templates",
            static_folder=Path(__file__).parent / "static")
balance = 500

flag = r'CTF{EXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG']


@app.route("/")
def index():
    return render_template('index.html', balance=balance)


@app.route('/buy', methods=['POST'])
def buy():
    global balance
    data = request.json
    dish_price = data['price']
    dish_name = data['dish']

    if balance >= dish_price:
        balance -= dish_price
        if dish_name == "Флаговая рыба на гриле":
            return jsonify({'alert': flag})  # Отправляем флаг для отображения в alert
        return jsonify({'success': True, 'balance': balance})
    else:
        return jsonify({'success': False, 'message': 'Недостаточно средств!'})


@app.get("/tips")
def get_tips():
    return render_template('tips.html', balance=balance)


@app.post('/tips')
def tips():
    global balance
    data = request.json
    tip_amount = int(data['amount'])

    if abs(tip_amount) <= balance:
        balance -= tip_amount
        return jsonify({'success': True, 'balance': balance})
    else:
        return jsonify({'success': False})


app.run(host="0.0.0.0", port=1337)
