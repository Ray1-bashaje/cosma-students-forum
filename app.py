from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Mfumo utatumia SQLite ukiwa kwenye kompyuta yako (Local)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jukwaa.db'
app.config['SECRET_KEY'] = 'cosma_secret_key_2026'
db = SQLAlchemy(app)

# Hapa tunatengeneza Jedwali la Database kwa ajili ya kuhifadhi Mijadala
class Mjadala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kichwa_cha_habari = db.Column(db.String(200), nullable=False)
    somo = db.Column(db.String(50), nullable=False)
    maelezo = db.Column(db.Text, nullable=False)
    tarehe = db.Column(db.DateTime, default=datetime.utcnow)

# Ukurasa Mkuu - Kuonyesha Maswali yote yaliyopo
@app.route('/')
def index():
    mijadala = Mjadala.query.order_by(Mjadala.tarehe.desc()).all()
    return render_template('index.html', mijadala=mijadala)

# Sehemu ya Kupokea Swali Jipya kutoka kwa Mwanafunzi
@app.route('/uliza', methods=['POST'])
def uliza():
    if request.method == 'POST':
        kichwa = request.form['kichwa']
        somo = request.form['somo']
        maelezo = request.form['maelezo']
        
        swali_jipya = Mjadala(kichwa_cha_habari=kichwa, somo=somo, maelezo=maelezo)
        db.session.add(swali_jipya)
        db.session.commit()
        return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Inatengeneza database kiotomatiki ikiwa haipo
    app.run(debug=True)