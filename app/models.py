from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for
import os


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
        # return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def _checkResizedImg(self, path_img, user_id):
        if os.path.isdir(f'{path_img}\\{user_id}') is True:
            return True
        else:
            return False

    def _get_actual_avatar(self, path_img, user_id):
        if self._checkResizedImg(path_img, user_id) is False:
            path_out = url_for('static', filename=r'avatars/standart_pic.png')
            return path_out
        else:
            all_pics = os.listdir(f'{path_img}\\{user_id}')
            if (type(all_pics) is list) and len(all_pics) > 1:
                pics_last = all_pics[-1]
            elif all_pics == []:
                path_out = url_for('static', filename=r'avatars/standart_pic.png')
                return path_out
            else:
                pics_last = all_pics[0]
            path_out = url_for('static', filename=f'avatars/{user_id}/{pics_last}')
            return path_out

    @staticmethod
    def count_pics(user_id):
        pic_path = os.getcwd() + r'\app\static\avatars'
        all_pics = os.listdir(f'{pic_path}\\{user_id}')
        return len(all_pics)

    def avatar(self):
        pic_path = os.getcwd() + r'\app\static\avatars'
        out = self._get_actual_avatar(pic_path, self.username)
        # print(out)
        return out


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
        # return f'<Post {self.body}>'
