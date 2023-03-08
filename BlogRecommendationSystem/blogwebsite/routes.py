import os
import secrets
from datetime import timedelta
import requests
from flask import render_template, url_for, flash, redirect, session, request
from PIL import Image
from blogwebsite.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from blogwebsite import app, User_Token, mail,api_link
from flask_mail import Message
from ProtectUserData import hash_user_pass


app.secret_key = "579162fdrfughhxtds4rd886fjur65edfg"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "redis"

posts = []

def get_blogs():
    if id in session:
        posts = requests.get(f"{api_link}/blogs/{session.get(id)}").json()
    else:
        posts = requests.get(f"{api_link}/blogs").json()
    return posts


@app.route("/")
@app.route("/home")
def home():
    # if session.get("id") is None:
    #     return redirect(url_for("login"))

    return render_template('home.html', posts=get_blogs())


@app.route("/about")
def about():
    # if session.get("id") is None:
    #     return redirect(url_for("login"))
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_name = form.username.data
        user_email = form.email.data
        user_pass=form.password.data
        hashed_password = hash_user_pass.get_password_hash(user_pass)
        resp = requests.post(f"{api_link}/register/name/{user_name}/email/{user_email}/password/{hashed_password}")
        message = resp.text
        flash(f'Your account has been created now you can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if id in session:
        return redirect(url_for("home"))
    elif form.validate_on_submit():
        user_email = form.email.data
        user_details = requests.get(f"{api_link}/login/email/{user_email}").json()
        user_pass=form.password.data
        hashed_password = hash_user_pass.get_password_hash(user_pass)

        if user_details['user_res'] == "Not Found":
            flash("User doesn't exist please register yourself first !!", 'danger')
            return redirect(url_for('register'))
        elif user_details['user_res'] == "Found" and user_details['user_pass'] == hashed_password:
            if form.remember.data is True:
                app.config["SESSION_PERMANENT"] = True
            else:
                app.permanent_session_lifetime = timedelta(weeks=5)

            session["id"] = user_details["user_id"]
            session["name"] = user_details["user_name"]
            session["email"] = user_details["user_email"]

            flash('You have logged in!', 'success')
            return redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    session.pop('name', None)
    session.pop('email', None)
    session.pop('id', None)
    return redirect(url_for("home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext[0] + f_ext[1]
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
def account():
    if session.get("name"):
        print("Session Started")
        form = UpdateAccountForm()
        if form.validate_on_submit():
            print(form.picture.data)
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                resp = requests.post(f"{api_link}/update/image/{picture_file}/id/{session['id']}").text
            if form.username.data != session["name"]:
                user_name = form.username.data
                resp = requests.post(f"{api_link}/update/name/{user_name}/id/{session['id']}").text
                session["name"] = user_name
            if form.email.data != session["email"]:
                user_email = form.email.data
                resp = requests.post(f"{api_link}/update/email/{user_email}/id/{session['id']}").text
                session["name"] = user_email
            flash('Your account has been updated!', 'info')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.username.data = session["name"]
            form.email.data = session["email"]
        user_id = session["id"]
        user_image = requests.get(f"{api_link}/image/id/{user_id}").json()
        image_file = url_for('static', filename='profile_pics/' + user_image['user_img'])
        return render_template('account.html', title='Account',
                               image_file=image_file, form=form)
    else:
        return redirect(url_for('home'))


def send_reset_email(user_id, user_email):
    token = User_Token.get_reset_token(user_id)
    msg = Message('Password Reset Request',
                  sender='no.reply.yakshblog@gmail.com',
                  recipients=[user_email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user_email = form.email.data
        user_detail = requests.get(f"{api_link}/id/email/{user_email}").json()
        send_reset_email(user_detail["user_id"], user_email)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User_Token.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user_pass=form.password.data
        hashed_password = hash_user_pass.get_password_hash(user_pass)
        res=requests.post(f'{api_link}/update/user/id/{user["user_id"]}/password/{hashed_password}').text
        print("Password Updated")
        flash('Your password has been updated! You are now able to log in', 'info')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/recommend", methods=['GET', 'POST'])
def recommend():
    # if session.get("name"):
    #     form = PostForm()
    #     if form.validate_on_submit():
    #         flash('Your Post has been Created','success')
    #         return(redirect(url_for('home')))
    return render_template('Recommend.html', posts=posts)
# else:
#     return redirect(url_for('home'))
