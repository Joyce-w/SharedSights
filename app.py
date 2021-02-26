from flask import Flask, request, render_template,  redirect, flash, session, json
import requests
import pdb
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from forms import UserSignup, NewPost
from secrets import MAPBOX_TOKEN

# app created 
app = Flask(__name__)

# specify that youre using postgres and a specific database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///shsi_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "wheredoyouwanttogo0217"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#call connect_db from models
connect_db(app)
    
# @app.before_request
# def token():
#     """Set token to session"""
#     session['token']=MAPBOX_TOKEN



@app.route('/')
def homepage():
    """Show homepage"""

    return render_template('homepage.html')

# login and signup
@app.route('/register', methods=["GET", "POST"])
def signup():
    """Display signup page"""

    form = UserSignup()

    if form.validate_on_submit():
        # signup user with User classmethod
        user = User.signup(display_name=form.display_name.data,
                            username=form.username.data,
                            password=form.password.data,
                            area=form.area.data)
        db.session.commit()
        return redirect("/")

    return render_template('/users/signup.html', form=form)

@app.route('/explore')
def explore():
    """Load map with pinned locations"""

    token=MAPBOX_TOKEN
    point = [
            [-118.1661, 33.9446],
            [-118.0, 32.9446],
            [-117.1661, 33.0],
            [34.0730663, -118.10917329999998]
    ]

    return render_template('map.html',token=token , point=point)

@app.route('/location-picker')
def find_location():
    """Find coordinates for post"""

    return render_template('find_coord.html')

@app.route('/new-post', methods=["GET","POST"])
def new_post():
    """Find coordinates for post"""

    form = NewPost()

    if form.validate_on_submit():
        # make new model
        
        title = form.title.data
        image = form.image.data
        description = form.description.data
        location = request.form['coords']
        user=1


        new_post = Post(title=title, image=image, description=description, location=location, user_id=user)
        db.session.add(new_post)
        db.session.commit()
        print(new_post)
        return redirect("/")
    else:
        return render_template('new_post.html', form=form)

    return render_template('new_post.html', form=form)
