from flask import render_template, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from . import bp
from .forms import RegistrationForm, LoginForm
from ...extensions import db
from ...models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        return redirect(url_for('main.index'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None:
            login_form.username.errors.append('Invalid username or password.')
            return render_template('auth/login.html', form=login_form)

        if user.check_password(login_form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            login_form.password.errors.append('Invalid username or password.')  

    return render_template('auth/login.html', form=login_form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            display_name=register_form.display_name.data,
            bio = None,
        )
        user.set_password(register_form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            register_form.username.errors.append('Username or email already exists.')
            return render_template('auth/register.html', form=register_form)

        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=register_form)

@bp.route('/logout')
def logout():
    session.pop('feed_ids', None)
    logout_user()
    return redirect(url_for('auth.login'))