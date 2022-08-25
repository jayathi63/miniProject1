
from sre_constants import CATEGORY
from unicodedata import category
from flask import Blueprint, redirect, render_template,request,flash,url_for
views=Blueprint('views',__name__)
from flask_login import login_required,current_user
from .models import Post,User,Comments,Likes
from .models import db
import sqlite3
from sqlalchemy import and_,desc

@views.route('/home')
@views.route('/')

@login_required
def home():
    rule = request.url_rule
    post=Post.query.order_by(desc(Post.count))
    print(post)
    return render_template('home.html',user=current_user,posts=post,rule=str(rule))

@views.route('/search',methods=['GET'])
def ntg():
    rule = request.url_rule
    search = request.args.get("srch")
    if not search:
            flash('search can not be empty',category="error")
            return redirect(url_for('views.home'))
    else:
        post=Post.query.filter(Post.post_text.like("%"+search+"%")).order_by(desc(Post.count))
        if not post.first():
            flash('no Match found',category="message")
        return render_template("srch.html",user=current_user,posts=post,search=search,rule=str(rule))

@login_required
@views.route('/post/<username>/search',methods=['GET'])
def ntgs(username):
    rule = request.url_rule
    search = request.args.get("srch")
    if not search:
            flash('search can not be empty',category="error")
            return redirect(url_for('views.home'))
    else:
        user=User.query.filter_by(username=username).first()
        post=Post.query.filter(and_(Post.post_text.like("%"+search+"%"),Post.author == user.id)).order_by(desc(Post.count))
        if not post.first():
            flash('no Match found',category="message")
        return render_template("srch.html",user=current_user,posts=post,search=search,rule=str(rule))

    '''srch = request.args.get("search")
    sqliteConnection = sqlite3.connect('./blog.db')
    cursor = sqliteConnection.cursor()
    sqlite_select_Query = "select * from post;"
    cursor.execute(sqlite_select_Query)
    posts = cursor.fetchall()
    return render_template('srch.html',srch = srch,posts = posts)'''



@views.route('/create_post',methods=['GET','POST'])
@login_required
def  create_post():
    rule = request.url_rule
    if request.method=="POST":
        text=request.form.get('post_text')
        if not text:
            flash('Post can not be empty',category="error")
        else:
            post=Post(post_text=text,author=current_user.id,count=0)
            db.session.add(post)
            db.session.commit()
            flash('post create',category="success")
    return render_template('create_post.html',user=current_user,rule=str(rule))

#for delete a post

@views.route("/delete_post/<id>")
@login_required
def delete_post(id):
    post=Post.query.filter_by(id=id).first()
    if not post:
        flash("flash does not exist",category="error")
    elif current_user.id !=post.author:
        flash("You are not right person to delete this messages",category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post Deleted",category="success")
    return redirect(url_for('views.home'))

# for specific user post to display

@views.route("/post/<username>")
@login_required
def posts(username):
    rule = request.url_rule
    user=User.query.filter_by(username=username).first()
    if not user:
        flash("no User with that username exist .",category="error")
        return redirect(url_for('views.home'))
    posts=user.posts
    return render_template("posts.html",user=current_user,posts=posts,username=username,rule=str(rule))

#create comments

@views.route('/create_comment/<post_id>',methods=['POST'])
@login_required
def create_comment(post_id):
    
    cmnt=request.form.get('commnet_text')
    if not cmnt:
        flash("Null comment is not Acceptable here",category="error")
    else:
        post=Post.query.filter_by(id=post_id)
        if post:
            comment=Comments(cm_text=cmnt,author=current_user.id,post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist',category="error")
    return redirect(url_for('views.home'))

#delete commentss

@views.route("/delete_comment/<cm_id>")
@login_required
def delete_comm(cm_id):
    comm=Comments.query.filter_by(id=cm_id).first()
    if not comm:
        flash("flash does not exist",category="error")
    elif current_user.id !=comm.author and current_user.id!=comm.post.author:
        flash("You are not right person to delete this messages",category="error")
    else:
        db.session.delete(comm)
        db.session.commit()
        flash("Comment Deleted",category="success")
    return redirect(url_for('views.home'))

#like button to display the like

@views.route("/like_post/<post_id>",methods=['GET'])
@login_required
def like_post(post_id):
    post=Post.query.filter_by(id=post_id)

    like=Likes.query.filter_by(author=current_user.id,post_id=post_id).first()
    if not post:
        flash("post does not exist",category="error")
    elif like:
        print("it is working")
        post.first().count-=1
        db.session.delete(like)
        db.session.commit()
    else:
        like=Likes(author=current_user.id,post_id=post_id)
        post.first().count+=1
        db.session.add(like)
        db.session.commit()
    return redirect(url_for('views.home'))