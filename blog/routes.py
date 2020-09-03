import os
import secrets
from flask import render_template, redirect, url_for, flash, request, abort
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewPostForm
from blog.moduls import User, Post
from blog import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
@login_required
def index():
    post = Post.query.all()
    return render_template("index.html", post=post)


@app.route("/about") 
@login_required
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Your account has been created! You are now able to log in', 'success')
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)
@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Email or Password Uncorrect', 'danger')
    return render_template("login.html", title="Login", form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    form_picture.save(picture_path)
    return picture_fn

@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if current_user.username != form.username.data or current_user.email != form.email.data or form.picture.data:
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your accout has been updated!', 'success')
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)



@app.route("/logout") 
def logout():   
    logout_user()
    return redirect(url_for('login'))


@app.route("/post/new", methods=["POST", "GET"])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", 'success')
        return redirect(url_for("index"))
    return render_template("new_post.html", title="New Post", form=form, legend="New Post")


@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title="Post", post=post)


@app.route("/post/<int:post_id>/update", methods=["POST", "GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if  post.author != current_user:
        abort(403)
    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for("index"))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("new_post.html", title="Update Post", form=form, legend="Update Post")


@app.route('/post/<int:post_id>/delete', methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted', 'success')
    return redirect(url_for('index'))

@app.route("/all")
def all():
    db.session.query(Model).delete()
    db.session.commit()
    return redirect(url_for('index'))