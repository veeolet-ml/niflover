import click
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import User

@click.group()
def user():
    pass

@user.command('create')
@click.option('--username', prompt=True)
@click.option('--email', prompt=True)
@click.option('--display-name', prompt='Display Name')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True) 
@with_appcontext
def create_user(username, email, display_name, password):
    user = User(
        username=username,
        email=email,
        display_name=display_name,
        bio=None,
    )
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
        click.echo(f'User {username} created successfully.')
    except IntegrityError:
        db.session.rollback()
        click.echo('Error: Username or email already exists.', err=True)

@user.command('seed')
@click.argument('count', type=int)
@with_appcontext
def seed_users(count):
    for i in range(count):
        username = f"user{i}"
        if User.query.filter_by(username=username).first():
            continue

        user = User(
            username=username,
            display_name=f"User {i}",
            email=f"user{i}@demo.com",
        )
        user.set_password("password123")

        db.session.add(user)

    try:
        db.session.commit()
        click.echo(f'Successfully seeded {count} users.')
    except IntegrityError:
        db.session.rollback()
        click.echo('Error: Could not seed users due to integrity error.', err=True)

@user.command('list')
@with_appcontext
def list_users():
    users = User.query.all()
    for user in users:
        click.echo(f'ID: {user.id}, Username: {user.username}, Email: {user.email}, Display Name: {user.display_name}')