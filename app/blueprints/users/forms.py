from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectMultipleField,
    PasswordField,
    FileField,
    BooleanField,
    SubmitField
)
from flask_login import current_user

from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from app.models import User

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    display_name = StringField('Display Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=1000)])

    hobbies = SelectMultipleField(
        'Hobbies',
        coerce=int,
    )

    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=8, max=128)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[Optional(), EqualTo('new_password', message='Passwords must match.')])

    photo0 = FileField('Photo 1', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])
    photo1 = FileField('Photo 2', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])
    photo2 = FileField('Photo 3', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])
    photo3 = FileField('Photo 4', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])
    
    delete0 = BooleanField('Delete Photo 1')
    delete1 = BooleanField('Delete Photo 2')
    delete2 = BooleanField('Delete Photo 3')
    delete3 = BooleanField('Delete Photo 4')

    submit = SubmitField('Update Profile')

    def validate_username(self, field):
        new_username = (field.data or '').strip()
        if new_username != current_user.username:
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user:
                raise ValidationError('This username is already taken. Please choose a different one.')
            
    def validate_email(self, field):
        new_email = (field.data or '').strip()
        if new_email != current_user.email:
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user:
                raise ValidationError('This email is already registered. Please use a different email address.')
            
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        if self.new_password.data or self.confirm_new_password.data:
            if not self.current_password.data:
                self.current_password.errors.append('Current password is required to set a new password.')
                return False
            if not current_user.check_password(self.current_password.data):
                self.current_password.errors.append('Current password is incorrect.')
                return False

        return True