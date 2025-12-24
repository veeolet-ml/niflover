from flask import render_template
from . import bp
from .forms import RegistrationForm, LoginForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        print("Form Submitted and Validated")

    return render_template('auth/register.html', form=register_form)