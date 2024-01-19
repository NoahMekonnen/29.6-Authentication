from flask import Flask, request, redirect, render_template, flash, session,jsonify
from models import db, connect_db, User,Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserForm,LoginForm,FeedbackForm

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Godalone1."
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()
# talk to mentor!!!

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=["GET","POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        email = form.data['email']
        first_name = form.data['first_name']
        last_name = form.data['last_name']

        new_user = User(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        return redirect('/secret')
    return render_template('register.html',form=form)

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session["username"] = user.username
            return redirect(f"users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login.html',form=form)

@app.route('/secret')
def secret():
    if "username" in session:
        return "You made it!"
    flash("You must be logged in!")
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>')
def user_detail(username):
    user = User.query.filter_by(username=username).first()
    if "username" in session:
        return render_template("detail.html",user=user)
    else:
        flash("You must be logged in")
        return redirect('/login')
    
@app.route('/users/<username>/delete',methods=["POST"])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user.username == session["username"]:
        db.session.delete(user)
        db.session.commit()

        session.pop("username")

        return redirect('/')
    flash("You must be logged in to delete your account")
    return redirect('/')

@app.route('/users/<username>/feedback/add',methods=["GET","POST"])
def create_feedback(username):
    if "username" in session:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.data['title']
            content = form.data['content']

            new_feedback = Feedback(title=title,content=content,username=username)
            db.session.add(new_feedback)
            db.session.commit()

            return redirect(f'/users/{username}')
        else:
            return render_template('feedback_form.html',form=form)
    return redirect('/')
@app.route('/feedback/<feedback_id>/update',methods=["GET","POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).first()

    if "username" not in session:
        return redirect('/')
    elif session["username"] == feedback.user.username:
        form = FeedbackForm()
        if form.validate_on_submit():

            title = form.data['title']
            content = form.data['content']

            feedback.title = title
            feedback.content = content
            feedback.username = feedback.user.username
            db.session.commit()

            return redirect(f'/users/{feedback.user.username}')
        else:
            return render_template('edit_feedback_form.html',form=form)

    else:
        return redirect(f'/users/{feedback.user.username}')

@app.route('/feedback/<feedback_id>/delete',methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).first()
    if "username" in session:
        if feedback.user.username == session["username"]:
            db.session.delete(feedback)
            db.session.commit()

            return redirect(f'/users/{feedback.user.username}')

        flash("You don't have permission to do that")
        return redirect('/')


    flash("You must be logged in ")
    return redirect('/')



