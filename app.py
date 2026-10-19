from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string 
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long = db.Column( "long",db.String())
    short = db.Column("short",db.String(3))

    def __init__(self, long, short):
        self.long = long
        self.short = short

with app.app_context():
    db.create_all()

def shorten_url():
    letter = string.ascii_lowercase + string.ascii_uppercase    
    while True:
        rand_letters = (random.choices(letter, k=3))
        rand_letters = ''.join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        url_received = request.form['nm']
        url_received = url_received.strip()

        if url_received == '':
            return "URL cannot be empty", 400

        found_url = Urls.query.filter_by(long=url_received).first()
        if found_url:
            return redirect(url_for('display_short_url', url=found_url.short))
        else:
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
        return redirect(url_for('display_short_url', url=short_url))
    else:
        return render_template("home.html")

@app.route('/display/<url>')
def display_short_url(url):
    return render_template("shorturl.html", short_url_display=url)

@app.route('/<short>')
def redirect_to_url(short):
    long_url = Urls.query.filter_by(short=short).first()

    if long_url:
        return redirect(long_url.long)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
