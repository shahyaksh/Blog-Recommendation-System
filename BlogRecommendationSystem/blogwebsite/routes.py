import os
import secrets
from calendar import week
from datetime import timedelta
from itsdangerous import TimedSerializer as Serializer
from flask import render_template, url_for, flash, redirect, session, request
from PIL import Image
from blogwebsite.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm,PostForm
from blogwebsite import app, mysql, bcrypt, User_Token, mail
from flask_mail import Message

conn = mysql.connect()
cursor = conn.cursor()
app.secret_key = "579162fdrfughhxtds4rd886fjur65edfg"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "redis"


def get_blogs_in_json_format(blogs_list: list):
    blog_json = []
    for blog in blogs_list:
        cursor.execute('select author_name from author where author_id=%s', [blog[1]])
        author_name = cursor.fetchone()[0]
        blog_dict = {
            "blog_id":blog[0],
            "authors": author_name,
            "content_link": blog[4],
            "title": blog[2],
            "content": blog[3],
            "image": blog[5],
            "topic": blog[6],
            "scrape_time": blog[7]
        }
        blog_json.append(blog_dict)
        blog_dict = {}
    return blog_json


def get_blogs_from_db():
    cursor.execute("""select * from blogs""")
    blogs_list = cursor.fetchall()
    blog_json = get_blogs_in_json_format(blogs_list)
    return blog_json



posts = get_blogs_from_db()


@app.route("/")
@app.route("/home")
def home():
    # if session.get("id") is None:
    #     return redirect(url_for("login"))
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    # if session.get("id") is None:
    #     return redirect(url_for("login"))
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_query = ''' insert into User_Profile(user_name,user_email,user_pass,user_pic)
                            values(%s,%s,%s,%s)'''
        user_info = (
            form.username.data, form.email.data, bcrypt.generate_password_hash(form.password.data),
            'default_profile_pic.jpg')
        # execute the query
        cursor.execute(user_query, user_info)
        conn.commit()
        flash(f'Your account has been created now you can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if session.get("id") is not None:
        return redirect(url_for("home"))
    elif form.validate_on_submit():
        cursor.execute(''' SELECT user_id,user_name,user_email,user_password from User_Profile 
                                        where user_email=%s''',
                       [form.email.data])
        user_pass = cursor.fetchone()

        if user_pass is None:
            flash("User doesn't exist please register yourself first !!", 'danger')
            return redirect(url_for('register'))
        elif user_pass and bcrypt.check_password_hash(user_pass[3], form.password.data):
            if form.remember.data is True:
                app.config["SESSION_PERMANENT"] = True
            else:
                app.permanent_session_lifetime = timedelta(weeks=5)

            session["id"] = user_pass[0]
            session["name"] = user_pass[1]
            session["email"] = user_pass[2]

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
                print(form.picture.data)
                cursor.execute(""" update user_profile set user_pic=%s where user_id=%s""",
                               [picture_file, session["id"]])
            if form.username.data != session["name"]:
                cursor.execute(""" update user_profile set user_name=%s where user_id=%s""",
                               [form.username.data, session["id"]])
                session["name"] = form.username.data
            if form.email.data != session["email"]:
                cursor.execute(""" update user_profile set user_email=%s where user_id=%s""",
                               [form.email.data, session["id"]])
                session["email"] = form.email.data
            conn.commit()
            print("Data Inserted")
            flash('Your account has been updated!', 'info')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.username.data = session["name"]
            form.email.data = session["email"]
        cursor.execute(""" select user_pic from user_profile where user_id=%s""", [session["id"]])
        user_image = cursor.fetchone()
        image_file = url_for('static', filename='profile_pics/' + user_image[0])
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
        cursor.execute(''' SELECT user_id from User_Profile 
                                        where user_email=%s''',
                       [form.email.data])
        user_detail = cursor.fetchone()
        print(user_detail)
        send_reset_email(user_detail[0], form.email.data)
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        cursor.execute(""" update user_profile set user_pass=%s where user_id=%s""",
                       (hashed_password, user[0]))
        conn.commit()
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
