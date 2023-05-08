import os
import secrets
import pathlib
from datetime import timedelta
import requests
from flask import render_template, url_for, flash, redirect, session, request, abort
from PIL import Image
from blogwebsite.forms import RegistrationForm, UpdateAccountForm
from blogwebsite import app, api_link
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app.secret_key = "579162fdrfughhxtds4rd886fjur65edfg"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "redis"

posts = []
liked_posts = []
favourite_blogs = []

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "1007230502107-u5mef247por579ibk07svp58hsuajrst.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def get_blogs():
    if id in session:
        posts = requests.get(f"{api_link}/blogs/{session['id']}").json()
    else:
        posts = requests.get(f"{api_link}/blogs").json()
    return posts


def like_blogs():
    liked_posts = requests.get(f"{api_link}/like/blogs/{session['id']}").json()
    if liked_posts != {'res': "Not Found"}:
        return liked_posts
    else:
        return None


def fav_blogs():
    favourite_blogs = requests.get(f"{api_link}/favourites/blogs/{session['id']}").json()
    if favourite_blogs != {'res': "Not Found"}:
        return favourite_blogs
    else:
        return None


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=get_blogs())


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/like")
def like():
    if session.get("name"):
        return render_template('like.html', posts=like_blogs())
    else:
        return redirect(url_for("login"))


@app.route("/fav")
def fav():
    if session.get("name"):
        return render_template('favourites.html', posts=fav_blogs())
    else:
        return redirect(url_for("login"))



@app.route("/register", methods=['GET', 'POST'])
def register():
    if session.get("email"):
        form = RegistrationForm()
        if form.validate_on_submit():
            user_name = form.username.data
            resp = requests.post(f"{api_link}/register/name/{user_name}/email/{session['email']}")
            user_profile = requests.get(f"{api_link}/login/email/{session['email']}").json()
            session["id"] = user_profile["user_id"]
            session["name"] = user_profile["user_name"]
            message = resp.text
            flash(f'Your account has been created successfully!!', 'info')
            return redirect(url_for('home'))
        return render_template('register.html', title='Register', form=form)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds = 2
    )
    user_details = requests.get(f"{api_link}/login/email/{id_info.get('email')}").json()

    if user_details['user_res'] == "Found":
        session["email"] = user_details["user_email"]
        session["name"] = user_details["user_name"]
        session["id"] = user_details["user_id"]
        app.permanent_session_lifetime = timedelta(days=1)
        flash('You have logged in!', 'success')
        return redirect(url_for('home'))
    else:
        print(id_info.get('email'))
        session['email'] = id_info.get('email')
        return redirect(url_for("register"))


@app.route("/logout")
def logout():
    session.pop('name', None)
    session.pop('email', None)
    session.pop('user_id', None)
    session.clear()
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

@app.route("/recommend", methods=['GET', 'POST'])
def recommend():
    if session.get("name"):
        recommeded_similar_blogs = requests.get(f"{api_link}/recommend/similar/blogs/{session['id']}").json()
        recommeded_blogs=[]
        if recommeded_similar_blogs!=[]:
            recommeded_blogs_by_collaborative_filtering = requests.get(f"{api_link}/recommend/blogs/using/rbm/{session['id']}").json()
            recommeded_blogs = recommeded_similar_blogs + recommeded_blogs_by_collaborative_filtering
        else:
            recommeded_blogs=requests.get(f"{api_link}/recommended/no/activity/blogs").json()
            flash('This are the top blogs this week for you!', 'success')
        return render_template('Recommend.html', posts=recommeded_blogs)
    else:
        return redirect(url_for('home'))
