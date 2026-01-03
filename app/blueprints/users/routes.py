import os
import uuid

from werkzeug.utils import secure_filename
from flask import redirect, render_template, url_for, abort, request, current_app
from flask_login import login_required, current_user

from app.models import User, Hobby, user
from app.extensions import db
from .forms import UpdateProfileForm
from .utils import save_photo_file, delete_photo_file, get_photo_by_position, normalize_photo_positions
from . import bp

@bp.get('/<string:username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('users/profile.html', user=user)

@bp.route('/<string:username>/update', methods=['GET', 'POST'])
@login_required
def update_profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    if user.id != current_user.id:
        abort(403)

    form = UpdateProfileForm()

    all_hobbies = Hobby.query.order_by(Hobby.category.asc(), Hobby.name.asc()).all()
    form.hobbies.choices = [(h.id, h.name) for h in all_hobbies]

    if request.method == 'GET':
        form.display_name.data = user.display_name
        form.username.data = user.username
        form.email.data = user.email
        form.bio.data = user.bio or ''
        form.hobbies.data = [h.id for h in user.hobbies]

    if form.validate_on_submit():
        user.display_name = form.display_name.data.strip()
        user.username = form.username.data.strip()
        user.email = form.email.data.strip().lower()
        user.bio = (form.bio.data or '').strip() or None

        selected_hobby_ids = set(form.hobbies.data or [])
        user.hobbies = Hobby.query.filter(Hobby.id.in_(selected_hobby_ids)).all()

        if form.new_password.data:
            user.set_password(form.new_password.data)

        max_photos = current_app.config['MAX_PHOTOS']
        slot_fields = [
            (0, form.photo0, form.delete0),
            (1, form.photo1, form.delete1),
            (2, form.photo2, form.delete2),
            (3, form.photo3, form.delete3),
        ]


        for pos, photo_field, delete_field in slot_fields[:max_photos]:
            photo = get_photo_by_position(user, pos)

            if delete_field.data:
                if photo:
                    delete_photo_file(photo.path)
                    db.session.delete(photo)
                continue

            if photo_field.data:
                old_path = photo.path if photo else None

                rel_path = save_photo_file(photo_field.data, user.username)

                if not photo:
                    user.add_photo(rel_path, pos)
                else:
                    photo.path = rel_path

                if old_path:
                    delete_photo_file(old_path)

        normalize_photo_positions(user)

        db.session.commit()

        return redirect(url_for('users.profile', username=user.username))
    
    return render_template('users/update_profile.html', form=form, user=user)