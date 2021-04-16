from flask import Blueprint, render_template, request, flash, redirect, url_for
from marvel_collection.forms import UserLoginForm
from marvel_collection.models import User, db

auth = Blueprint('auth',__name__,template_folder='auth_templates')

@auth.route('/signup',methods=['GET','POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            print(name, email, password)
            
            user = User(email, name = name, password = password)
            db.session.add(user)
            db.session.commit()

            flash(f'Welcome, {name}.\nYou have successfully created a user account: {email}', 'user-created')

            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form Inputs')

    return render_template('signup.html', form = form)

@auth.route('/signin',methods=['GET','POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first() 

            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash(f'Welcome back, {logged_user.name}! You were successfully logged in.', 'auth-sucess')
                return redirect(url_for('site.index'))
            else:
                flash('Your email/password is incorrect', 'auth-failed')

                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signin.html', form = form)

# @auth.route('/logout')
# # @login_required #need to import
# def logout():
#     # logout_user() #need to import
#     return redirect(url_for('site.home'))