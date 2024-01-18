from flask import Flask, request, redirect, render_template, flash, session,jsonify
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserForm,LoginForm

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Godalone1."
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
# db.create_all()

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=["GET","POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.data.username
        password = form.data.password
        email = form.data.email
        first_name = form.data.first_name
        last_name = form.data.last_name

        new_user = User(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        return redirect('/secret')
    return render_template('register.html',form=form)

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data.username
        password = form.data.password

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return redirect(f"users/{user}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login.html',form=form)

@app.route('/secret')
def secret():
    return "You made it!"

@app.route('logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/users/<username>')
def user_detail(username):
    user = User.query.filter_by(username=username).first()
    if "user_id" in session:
        return render_template("detail.html",user=user)
    else:
        return redirect('/login')
