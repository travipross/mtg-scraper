from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from requests import request
import re
from bs4 import BeautifulSoup

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

card_ownership = db.Table(
    'card_ownership',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('card_id', db.Integer, db.ForeignKey('card.id'))
)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    setname = db.Column(db.String, index=True)
    foil = db.Column(db.Boolean, default=False)
    url = db.Column(db.String, index=True)
    img_url = db.Column(db.String)
    purchase_price = db.Column(db.Float)
    lowest_price = db.Column(db.Float)
    highest_price = db.Column(db.Float)
    current_price = db.Column(db.Float)
    time_updated = db.Column(db.DateTime)
    daily_change = db.Column(db.Float)
    weekly_change = db.Column(db.Float)

    def from_dict(self, data):
        for key in ['name', 'setname', 'foil']:
            setattr(self, key, data[key])
        for key in ['purchase_price', 'current_price', 'lowest_price', 'highest_price', 'time_updated', 'daily_change', 'weekly_change']:
            setattr(self, key, data.get(key))

    def to_dict(self):
        data = {
            'name': self.name,
            'setname': self.setname,
            'foil': self.foil,
            'url': self.url
        } 
        return data

    @staticmethod
    def _encode_for_url_without_escapes(card_name):
        if card_name is None:
            raise ValueError("Shit's fucked, yo")
        _chars_to_remove = ["\'", ","]
        name_url = re.sub(" ", "+", card_name)
        name_url = re.sub("|".join(_chars_to_remove), "", name_url)
        return name_url

    def build_url(self):
        name_url = self._encode_for_url_without_escapes(self.name) + "#paper"
        set_url = self._encode_for_url_without_escapes(self.setname)
        if self.foil:
            set_url += ":Foil"
        url = "/".join(["https://www.mtggoldfish.com/price", set_url, name_url])
        r = request('get', url)
        if r.status_code == 200:
            self.url = url
            soup = BeautifulSoup(r.text, 'html.parser')
            img = soup.find("img", class_="price-card-image-image")
            if img is not None:
                self.img_url = img['src']

    def __repr__(self):
        return '<Card {}>'.format(self.name)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )
    cards = db.relationship("Card", secondary=card_ownership)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(id)