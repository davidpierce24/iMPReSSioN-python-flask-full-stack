from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

# Route to render the login and registration page
@app.route('/login/page')
def login_page():
    if 'user_id' in session:
        return redirect('/user/page')

    return render_template("login.html")


# Route to render the login and registration page
@app.route('/register/page')
def register_page():
    if 'user_id' in session:
        return redirect('/user/page')

    return render_template("register.html")


# Route to process user registration
@app.route('/register', methods=["POST"])
def register():

    # validate user
    if not User.validate_user(request.form):
        return redirect('/register/page')


    # then if valid, add to DB
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        'username': request.form['username'],
        'email': request.form['email'],
        'password': pw_hash
    }

    user_id = User.add_user(data)

    session['user_id'] = user_id
    session['username'] = request.form['username']


    return redirect('/user/page')



# Route to process user login
@app.route('/login', methods=["POST"])
def login():

    email_input = { "email" : request.form["email"] }
    users = User.get_by_email(email_input)
    
    if len(users) != 1:
        flash("Invalid Email/Password")
        return redirect('/login/page')

    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login/page')

    session['user_id'] = user.id
    session['username'] = user.username

    return redirect('/user/page')


# Route to successful registration or login
@app.route('/user/page')
def success():
    if 'user_id' not in session:
        flash("You must log in to view this page")
        return redirect('/login/page')

    print (session['user_id'])


    return render_template("user_page.html")



# Route to logout user
@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')