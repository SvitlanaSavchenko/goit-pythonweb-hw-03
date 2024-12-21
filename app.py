from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['JSON_PATH'] = os.path.join('storage', 'data.json')

# Перевірка, чи існує data.json
if not os.path.exists(app.config['JSON_PATH']):
    with open(app.config['JSON_PATH'], 'w') as file:
        json.dump({}, file)

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Сторінка відправки повідомлення
@app.route('/message.html')
def message_form():
    return render_template('message.html')

# Обробка форми
@app.route('/message', methods=['POST'])
def handle_message():
    username = request.form.get('username')
    message = request.form.get('message')
    timestamp = datetime.now().isoformat()

    if username and message:
        with open(app.config['JSON_PATH'], 'r+') as file:
            data = json.load(file)
            data[timestamp] = {"username": username, "message": message}
            file.seek(0)
            json.dump(data, file, indent=4)
        return redirect(url_for('index'))
    return "Invalid data", 400

# Сторінка читання повідомлень
@app.route('/read')
def read_messages():
    with open(app.config['JSON_PATH'], 'r') as file:
        messages = json.load(file)
    return render_template('read.html', messages=messages)

# Статичні файли
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Обробка помилок 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(port=3000, debug=True)
