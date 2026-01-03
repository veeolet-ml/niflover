import click
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Hobby


@click.group()
def hobby():
    """Hobby management commands."""
    pass


@hobby.command("create")
@click.option("--name", prompt=True)
@click.option("--category", prompt=True)
@with_appcontext
def create_hobby(name: str, category: str):
    """Create a single hobby."""
    hobby_obj = Hobby(name=name, category=category)

    db.session.add(hobby_obj)
    try:
        db.session.commit()
        click.echo(f'Hobby "{name}" created successfully.')
    except IntegrityError:
        db.session.rollback()
        click.echo('Error: Hobby name already exists (or another integrity error occurred).', err=True)


@hobby.command("list")
@with_appcontext
def list_hobbies():
    """List all hobbies."""
    hobbies = Hobby.query.order_by(Hobby.id.asc()).all()
    if not hobbies:
        click.echo("No hobbies found.")
        return

    for h in hobbies:
        click.echo(f"ID: {h.id}, Name: {h.name}, Category: {h.category}")

@hobby.command("create_from")
@click.argument("filepath", type=click.Path(exists=True, dir_okay=False, readable=True, path_type=str))
@with_appcontext
def create_hobbies_from_file(filepath: str):
    """
    Create hobbies from a text file.

    Format:
      - Lines starting with # are categories (e.g. #Development)
      - Other non-empty lines are hobby names under the current category
      - Existing hobbies are skipped
    """
    current_category: str | None = None
    created = 0
    skipped_existing = 0
    skipped_invalid = 0

    # Optional: reduce DB queries by caching existing hobby names (case-insensitive)
    existing = {
        (name or "").strip().lower()
        for (name,) in db.session.query(Hobby.name).all()
    }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line_no, raw in enumerate(f, start=1):
                line = raw.strip()

                # skip empty lines
                if not line:
                    continue

                # category line
                if line.startswith("#"):
                    current_category = line[1:].strip()
                    if not current_category:
                        click.echo(f"Line {line_no}: empty category header; ignoring.", err=True)
                        current_category = None
                        skipped_invalid += 1
                    continue

                # hobby line (must have a category set)
                if not current_category:
                    click.echo(
                        f'Line {line_no}: hobby "{line}" has no category header above it; skipping.',
                        err=True,
                    )
                    skipped_invalid += 1
                    continue

                hobby_name = line
                key = hobby_name.lower()

                if key in existing:
                    skipped_existing += 1
                    continue

                db.session.add(Hobby(name=hobby_name, category=current_category))
                existing.add(key)
                created += 1

        db.session.commit()
        click.echo(
            f"Done. Created {created} hobbies, skipped {skipped_existing} existing, "
            f"skipped {skipped_invalid} invalid."
        )

    except IntegrityError:
        db.session.rollback()
        click.echo(
            "Error: Could not create hobbies due to an integrity error. "
            "No changes were committed for this run.",
            err=True,
        )
    except OSError as e:
        db.session.rollback()
        click.echo(f"Error reading file: {e}", err=True)