# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from PIL import Image
import hashlib
import os


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Домашняя страница', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегестрировались на сайте !')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    if request.method == 'POST':
        FileNotFound = None
        try:
            file = request.files['file']
            filename = secure_filename(file.filename)
            path_images = os.getcwd() + r'\tmp'
            file.save(os.path.join(path_images, filename))
            _resize(path_img=path_images + f'\\{filename}', size=200,
                    user_id=user.id, pics_before=User.count_pics(user_id=user.id))
            print(user.id)
            FileNotFound = False
        except FileNotFoundError:
            FileNotFound = True
        finally:
            request.close()
            return render_template('user.html', user=user, posts=posts,
                                   Error_FileNotFoundError=FileNotFound)
    return render_template('user.html', user=user, posts=posts)


def _resize(path_img, size, user_id, pics_before):
    img = Image.open(path_img)
    nex_x, new_y = int(size / 2), int(size / 2)
    img = img.resize((nex_x, new_y), Image.ANTIALIAS)
    img_name = f'{user_id}, pic-{pics_before + 1}.png'
    path_endfile = os.getcwd() + f'\\app\\static\\avatars\\{user_id}\\' + img_name
    if len(os.listdir(os.getcwd() + f'\\app\\static\\avatars\\{user_id}')) > 0:
        hashed_already = set([hashlib.md5(Image.open(os.getcwd() +
                             f'\\app\\static\\avatars\\{user_id}\\{i}').tobytes()).hexdigest()
                              for i in os.listdir(os.getcwd() + f'\\app\\static\\avatars\\{user_id}')])
        hash_uploaded = hashlib.md5(img.tobytes()).hexdigest()
        if hash_uploaded in hashed_already:
            img.close()
        else:
            img.save(fp=path_endfile)
    else:
        img.save(fp=path_endfile)
    return path_endfile
