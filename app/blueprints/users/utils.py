import os
import uuid

from werkzeug.utils import secure_filename
from flask import redirect, render_template, url_for, abort, request, current_app
from app.extensions import db

def ensure_upload_dir():
    upload_dir = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

def save_photo_file(file_storage, username):
    ensure_upload_dir()

    filename = secure_filename(file_storage.filename or 'photo')
    ext = os.path.splitext(filename)[1].lower() or '.jpg'
    unique_filename = f"{username}_{uuid.uuid4().hex}{ext}"

    rel_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    abs_path = os.path.join(current_app.static_folder, rel_path)

    file_storage.save(abs_path)

    return rel_path

def delete_photo_file(rel_path):
    if not rel_path:
        return
    
    abs_path = os.path.join(current_app.static_folder, rel_path)

    if os.path.exists(abs_path):
        os.remove(abs_path)

def get_photo_by_position(user, pos):
    for photo in user.photos:
        if photo.position == pos:
            return photo
    return None

def normalize_photo_positions(user):
    photos = sorted(user.photos, key=lambda p: p.position)
    for index, photo in enumerate(photos[:current_app.config['MAX_PHOTOS']]):
        photo.position = index

    for photo in photos[current_app.config['MAX_PHOTOS']:]:
        db.session.delete(photo)