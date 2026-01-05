import click
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Game

@click.group()
def game():
    """Game management commands."""
    pass

@game.command("create")
@click.option("--title", prompt=True)
@click.option("--slug", prompt=True)
@with_appcontext
def create_game(title: str, slug: str):
    """Create a single game."""
    game_obj = Game(title=title, slug=slug)

    db.session.add(game_obj)
    try:
        db.session.commit()
        click.echo(f'Game "{title}" created successfully.')
    except IntegrityError:
        db.session.rollback()
        click.echo('Error: Game title or slug already exists (or another integrity error occurred).', err=True)

@game.command("list")
@with_appcontext
def list_games():
    """List all games."""
    games = Game.query.order_by(Game.id.asc()).all()
    if not games:
        click.echo("No games found.")
        return

    for g in games:
        click.echo(f"ID: {g.id}, Title: {g.title}, Slug: {g.slug}")