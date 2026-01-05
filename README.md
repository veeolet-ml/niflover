# [nifLover](https://github.com/veeolet-ml/niflover)

`nifLover` is a minigame-driven dating app built with Flask and Pygame-CE.

Users can sign up, customize their profile by adding photos, hobbies and a bio, and swipe through different people to search for their other half! The matchmaking algorithm centers around finding people with similar interests and gaming abilities, which leads to the other parts of the project: the minigames (Snake, BlockBlast and Dino), which are launched in their own Pygame windows and submit high scores to the server, to be showcased in the user's profile.

## Features
- Email/password auth, session-based login, and profile editing with bio, hobbies, and up to four photos
- Swipe-style feed with like/pass; mutual likes create a match and unlock messaging
- Match inbox with conversations
- Built-in mini-games launched from the web UI
- Admin-friendly CLI commands to interact with the database

## Stack
- Flask, Flask-Login, Flask-Migrate, SQLAlchemy
- SQLite by default (configurable via `DATABASE_URL`)
- Pygame mini-games for scoring

## Quickstart
```bash
git clone git@github.com:veeolet-ml/niflover.git
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# make sure to change secret key
mv .env.example .env

# skip if db already present
flask db init

# apply migrations
flask db upgrade

# run the web app
python run.py
```

## Configuration
Environment variables (see `app/config.py` for defaults):
- `SECRET_KEY` – Flask session secret (default: `gigel`).
- `DEBUG` – `True`/`False` toggle for debug mode (default: `False`).
- `DATABASE_URL` – SQLAlchemy URL (default: `sqlite:///niflover.db`, stored in the repo root).
- `UPLOAD_FOLDER` – Relative path under `app/static/` for profile photos (default: `uploads/user_photos`).
- `MAX_PHOTOS` – Max number of photos per user (default: 4). Note: App currently only admits 4 because of database structure constraints
- `MAX_CONTENT_LENGTH` – Upload limit in bytes (default: 16 MB).

## Running the mini-games
Games open in their own window and submit scores back to the Flask server at `/game/submit_score`.
On your profile page, click a game to launch; your username is passed automatically.

## CLI helpers
All commands use `flask <group> <command> ...`.
- Users: `user create`, `user seed <count>`, `user list`, `user actions <username>`, `user matches <username>`
- Hobbies: `hobby create`, `hobby list`, `hobby create_from <file>`
- Games: `game create`, `game list`

## Project structure (high level)
- `app/` – Flask app factory, blueprints (`auth`, `main`, `matches`, `users`), models, CLI commands, static assets.
- `games/` – Pygame mini-games (`snake`, `blockblast`, `dino`) that post scores to the Flask server.
- `migrations/` – Alembic migration scripts.
- `run.py` – Entry point for the Flask app.

## Database
SQLite is the default; run `flask db upgrade` to apply migrations. To reset locally, remove the SQLite file and rerun the upgrade. For other databases, set `DATABASE_URL` accordingly. Hobbies and Games must also be entered manually.

## Contributions

### Val (veeolet-ml)
- implemented Flask app (frontend + backend)
- integrated server with the minigames (non-blocking subprocess launch from frontend buttons via server api call, request-style submit from game with username provided by the subprocess launch)
- difficulties & solutions:
  - fast-changing and growing database models -> learned `flask_migrate`
  - non-blocking game launches -> learned to use `subprocess` and `argparser`
  - path handling -> learned `pathlib`
  - photo handling -> used `secure_filename` and `uuid` to generate good filenames

### Paul (PaulBurca2005)
- implemented [BlockBlast](./games/blockblast/README.md)
- implemented [Dino](./games/dino/README.md)
- difficulties & solutions:
  - coming up with the Block object design -> applying OOP principles to build a generic block
  - hitbox issues in the Dino game -> building custom hitboxes from the Pygame library
  - making the Dino game random enough -> using the `random` library accordingly
  - the lack of sprite for the Dino projectile -> drawing it on [pixilart.com](https://www.pixilart.com/draw)

### Luca (Lucapetre)
- implemented [Snake](./games/snake/README.md)
- implemented user matchmaking algorithm
- difficulties & solutions:
  - designing the game such that the code is extensible and readable -> using type annotations and OOP principles
  - music and sounds were too loud -> searching through the documentation for `set_volume()`
  - using the database models code to implement the matchmaking algorithm with no previous interaction -> reading its good documentation