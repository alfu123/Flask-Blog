from datetime import datetime
# from flask import render_template,flash,redirect,url_for
# from flask import Flask, render_template, url_for,flash,redirect
# from flask.forms import RegistrationForm, LoginForm
# from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask2 import db,login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# app=Flask(__name__)
# app.config["SECRET_KEY"] = 'a9ef0101ef2191d5de7d6c7977dca2c0'
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
# db = SQLAlchemy(app)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts=db.relationship('Post', backref='author',lazy="dynamic")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(100), nullable=False)
    date_posted= db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


# posts=[{
#     "author":"Alfahad",
#     "title":"Blog Post1",
#     "content":"First post content",
#     "date_posted":"April 20, 2020",
# },
#      {
#     "author":"Harry",
#     "title":"Blog Post2",
#     "content":"Second Post Content",
#     "date_posted":"April 20,2020"
#      }]
# @app.route("/")
# def home():
#     return render_template('home.html',posts=posts)
# @app.route("/about")
# def about():
#     return render_template('about.html',title="About")
# @app.route("/register",methods=["GET","POST"])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash(f"Account created for {form.username.data}!",'success')
#         return redirect(url_for("home"))
#     return render_template('register.html', title="Register", form=form)
#
# @app.route("/login",methods=["GET","POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data=="admin@blog.com" and form.password.data=="password":
#             flash("You have been logged in!", "success")
#             return redirect(url_for("home"))
#         else:
#             flash("Login Unsuccessful Pleas check Username and Password","danger")
#     return render_template('login.html', title="login", form=form)
# app.run(debug=True)