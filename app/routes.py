# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from flask import jsonify

from werkzeug.urls import url_parse
from app.models import User
from app.models import Post
from app import app
from app import db
from app.forms import RegistrationForm
from app.forms import LoginForm
from app.forms import EditProfileForm
from app.forms import PostForm

from app.pristav import zapros_f
from app.pristav import zapros_f_s
from app.pristav import zapros_f_r

from datetime import datetime

import requests
import json

url = "https://api.telegram.org/bot744645999:AAE8JuHsXj2RgpHZvicoFjmwe3GQ12VfU44/"

def get_updates_json(request):  
    response = requests.get(request + 'getUpdates')
    return response.json()
 
def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id

def get_last_mes_text(update):  
    text = update['message']['text']
    return text

def get_last_mes_user(update):  
    user = update['message']['from']['first_name']
    return user

 
def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])                                     
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
   form = PostForm()
   if form.validate_on_submit():
        post = Post.query.filter_by(author=current_user).order_by(Post.timestamp.desc()).first()
        if post :
            post.region = form.region.data
            post.lastname = form.lastname.data
            post.firstname = form.firstname.data
        else :
            post = Post(region=form.region.data, lastname = form.lastname.data, firstname = form.firstname.data, author=current_user)
            db.session.add(post)      
        db.session.commit()
        flash('Запрос создан')
        return redirect(url_for('index'))
   page = request.args.get('page', 1, type=int)
   posts=Post.query.filter_by(author=current_user).order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
   next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
   prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
   return render_template('index.html', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/telehist')
@login_required
def telehist():
   updates = get_updates_json(url)
   if updates['ok']:
     results= updates['result']
     posts = []
     for update in results: 
       posts.append(
        {
            'chat_id': update['message']['chat']['id'],
            'author': {'username': update ['message']['from']['first_name']},
            'message': update['message']['text']
        } )
   else:  posts = [{'Сегодня сообщений не было'}] 
   return render_template('telehist.html', posts=posts)

@app.route('/zapros_pristav_f', methods=['POST'])
@login_required
def zapros_pristav_f():
    return jsonify({'task': zapros_f(request.form['region'],
                                      request.form['firstname'],
                                      request.form['lastname'])})

@app.route('/zapros_pristav_s', methods=['POST'])
@login_required
def zapros_pristav_s():
    return jsonify({'progress': zapros_f_s(request.form['task'])})

@app.route('/zapros_pristav_r', methods=['POST'])
@login_required
def zapros_pristav_r():
    req=zapros_f_r(request.form['task'])
    p = Post.query.filter_by(id = int(request.form['post_id'])).first()
    p.otvet_prist = json.dumps(req['result'])
    p.status_prist = len(req['result'])
    db.session.commit()
    status ='<a href="'+ url_for('otvet_prist', post_id = request.form['post_id'])+'">Найдено ИП: ' + str(len(req['result'])) + '</a>'
    return jsonify({ 'status': status, 'result': req })


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

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
        flash('Поздравляем, регистрация прошла успешно!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.get_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None    
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/otvet_prist/<post_id>')
@login_required
def otvet_prist(post_id):
    p = Post.query.filter_by(id = post_id).first_or_404()
    #page = request.args.get('page', 1, type=int)
    return render_template('otvet_prist.html', posts=json.loads(p.otvet_prist))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
