import click
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from app.extensions import db
from app.models import User, UserAction, ActionType, Match

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

@user.command('actions')
@click.argument('username')
@with_appcontext
def show_user_actions(username):
    """
    Show all user actions (sent and received) for a given user.
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f'User "{username}" not found.', err=True)
        return

    sent = UserAction.query.filter_by(actor_id=user.id).all()
    received = UserAction.query.filter_by(target_id=user.id).all()

    click.echo(f'\nUser actions for "{user.username}" (ID {user.id})')
    click.echo('=' * 40)

    click.echo('\nSent actions:')
    if not sent:
        click.echo('  (none)')
    for ua in sent:
        target = User.query.get(ua.target_id)
        click.echo(f'  -> {ua.action.name} → {target.username} (ID {target.id})')

    click.echo('\nReceived actions:')
    if not received:
        click.echo('  (none)')
    for ua in received:
        actor = User.query.get(ua.actor_id)
        click.echo(f'  <- {ua.action.name} ← {actor.username} (ID {actor.id})')

@user.command('matches')
@click.argument('username')
@with_appcontext
def show_user_matches(username):
    """
    Show all matches that involve a given user (as user_a or user_b).
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f'User "{username}" not found.', err=True)
        return

    matches = (
        Match.query
        .filter(or_(Match.user_a_id == user.id, Match.user_b_id == user.id))
        .order_by(Match.created_at.desc())
        .all()
    )

    click.echo(f'\nMatches for "{user.username}" (ID {user.id})')
    click.echo('=' * 40)

    if not matches:
        click.echo('  (none)')
        return

    for m in matches:
        other_id = m.user_b_id if m.user_a_id == user.id else m.user_a_id
        other = User.query.get(other_id)
        other_label = f'{other.username} (ID {other.id})' if other else f'UserID {other_id}'

        created = m.created_at.isoformat(sep=' ', timespec='seconds') if getattr(m, "created_at", None) else "N/A"
        click.echo(f'  ♥ {other_label}  | match_id={m.id} | created_at={created}')
