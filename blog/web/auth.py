from flask import Blueprint, flash, render_template,redirect,url_for,request
from .import db
from .models import User,Post
from flask_login import current_user, login_user,logout_user,login_required
from werkzeug.security import generate_password_hash,check_password_hash
auth=Blueprint("auth",__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    rule = request.url_rule
    if request.method=='POST':
        email=request.form.get("email")
        password=request.form.get("pswd")
        user=User.query.filter_by(email=email).first()
        if user:
            print(user.email)
            print(password)
            print(user.password)
            if check_password_hash(user.password,password):
                flash("Logged In!",category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('password is incorrect',category='error')
        else:
            flash('EMail does not exist',category='error')
    return render_template('login.html',user=current_user,rule=str(rule))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        rule = request.url_rule
        email=request.form.get("email")
        username=request.form.get("username")
        password1=request.form.get("password1")
        password2=request.form.get("password2")
        email_exists=User.query.filter_by(email=email).first()
        user_exists=User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already is use.',category='error')
        elif user_exists:
            flash('Username is already exists.',category='error')
        elif password1 != password2:
            print(password1)
            print(password2)
            flash('password is not matching',category='error')
        elif len(username)<3:
             flash('Username is too short',category='error')
        elif len(password1)<3:
             flash('password is too short',category='error')
        else:
            new_user=User(email=email,username=username,password=generate_password_hash(password1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('user created')
            return redirect(url_for('views.home'))
    return render_template('sign_up.html',user=current_user,rule=str(rule))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))