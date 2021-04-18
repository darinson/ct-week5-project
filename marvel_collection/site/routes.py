from flask import Blueprint, render_template, request, flash, redirect, url_for
from marvel_collection.forms import NewCharacterEntry
from marvel_collection.models import User, Character, db
from flask_login import login_required

site = Blueprint('site',__name__,template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/collection')
def collection():
    return render_template('collection.html')

@site.route('/collection/add', methods = ['GET','POST'])
@login_required
def addcharacter():
    form = NewCharacterEntry()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            description = form.description.data
            comics_appeared_in = form.comics_appeared_in.data
            super_power = form.super_power.data
            user_token = form.user_token.data
            print("Character: ", name, description, comics_appeared_in, super_power)
            print("For User #", user_token)

            #need help, how to add current user (already signed in)'s token without having them manually input the token?
            character = Character(name = name, description = description, comics_appeared_in = comics_appeared_in, super_power = super_power, user_token = user_token)

            logged_user = User.query.filter(User.token == user_token).first()

            if logged_user:
                db.session.add(character)
                db.session.commit()
                flash(f"Successfully added {character.name} to {logged_user.name}'s Collection!", 'add-success')
                return redirect(url_for('site.addcharacter'))
            else:
                flash('User token not valid. Please enter valid token', 'token-failed')
                return redirect(url_for('site.addcharacter'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('add.html', form = form)

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')