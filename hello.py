from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import re
from datetime import datetime
# import dns.resolver
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    
    
    email = request.form['textInput']
    email= email.strip().lower()
    new_user = User(email=email)
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    existing_user=User.query.filter_by(email=email).first()
    if existing_user is not None:
        valid=False
    if valid:



    # Добавление email в базу
    
        db.session.add(new_user)
        db.session.commit()

        flash('Спасибо за подписку!', 'success')
    return redirect(url_for('index'))

if __name__ == 'main':
    #with app.app_context():
    #   db.create_all()  # Создание таблиц в базе данных
    app.run(debug=True)