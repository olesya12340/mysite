from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

# Модель базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

# Главная страница с формой
@app.route('/')
def index():
    return render_template('index.html')

# Обработка формы
@app.route('/submit', methods=['POST'])
def submit_email():
    email = request.form.get('textInput', '').strip().lower()

    # Регулярное выражение для проверки email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'

    # Проверка: email не пустой и соответствует формату
    if not email or not re.match(email_regex, email):
        return redirect(url_for('error_page'))

    # Проверка: существует ли уже email в базе данных
    if User.query.filter_by(email=email).first():
        return redirect(url_for('error_page'))

    # Добавление email в базу данных
    new_user = User(email=email)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('success_page'))

# Страница успешной подписки
@app.route('/success')
def success_page():
    return render_template('success.html')

# Страница ошибки
@app.route('/error')
def error_page():
    return render_template('error.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц
    app.run(debug=True)
