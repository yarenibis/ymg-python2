from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Personel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50))
    soyad = db.Column(db.String(50))
    pozisyon = db.Column(db.String(50))

@app.route('/api/personel', methods=['GET'])   #tüm personelleri listeler
def get_personel():
    data = Personel.query.all()
    return jsonify([{'id': p.id, 'ad': p.ad, 'soyad': p.soyad, 'pozisyon': p.pozisyon} for p in data])

@app.route('/api/personel', methods=['POST'])
def add_personel():
    data = request.get_json()

    if not all(k in data for k in ('ad', 'soyad', 'pozisyon')):
        return jsonify({'error': 'Eksik bilgi gönderildi'}), 400

    p = Personel(ad=data['ad'], soyad=data['soyad'], pozisyon=data['pozisyon'])
    db.session.add(p)
    db.session.commit()
    return jsonify({'id': p.id, 'ad': p.ad, 'soyad': p.soyad, 'pozisyon': p.pozisyon}), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port='9090')
