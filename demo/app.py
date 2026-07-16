"""
flask-selfheal live demo — EuroPython 2026

A tiny "conference portal" used to demo flask-selfheal's resolvers, chained
together in a single app:

    1. AliasMappingResolver   -> instant redirects for known renamed pages
    2. FlaskRoutesResolver    -> fixes typos in top-level pages (schedule, sponsors, ...)
    3. TalkSlugResolver       -> a custom resolver (wraps DatabaseResolver) that heals
                                 /talks/<slug> URLs: missing words, reordered words,
                                 wrong case, and bare id/keyword fragments.

Run it:
    pyenv shell selfheal-demo
    python app.py
Then open http://127.0.0.1:5000/ and try the broken URLs from cheatsheet.md.
"""

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_selfheal import SelfHeal
from flask_selfheal.resolvers import (
    BaseResolver,
    AliasMappingResolver,
    FlaskRoutesResolver,
    DatabaseResolver,
)
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'demo.db')}"
db = SQLAlchemy(app)


class Talk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    speaker = db.Column(db.String(120), nullable=False)


TALKS = [
    {
        "slug": "self-healing-urls-explained-hollis",
        "title": "The Self-Healing Web: Designing Resilient, Typo-Proof URLs",
        "speaker": "Dominic Hollis",
    },
    {
        "slug": "typed-python-at-scale-42",
        "title": "Typed Python at Scale",
        "speaker": "A. N. Other",
    },
    {
        "slug": "async-flask-patterns-17",
        "title": "Async Flask Patterns",
        "speaker": "B. Speaker",
    },
]


# ---------------------------------------------------------------------------
# A custom resolver: flask-selfheal resolvers are just classes with a
# `.resolve(path) -> str | None` method. Here we wrap DatabaseResolver so
# talk slugs can live under /talks/<slug> while everything else in this app
# redirects from the site root - SelfHeal only supports one redirect_pattern
# per app, so this resolver re-adds the "talks/" prefix itself.
# ---------------------------------------------------------------------------
class TalkSlugResolver(BaseResolver):
    PREFIX = "talks/"

    def __init__(self, model, **kwargs):
        self._inner = DatabaseResolver(model, **kwargs)

    def resolve(self, path: str) -> str | None:
        if not path.startswith(self.PREFIX):
            return None
        match = self._inner.resolve(path[len(self.PREFIX):])
        return f"{self.PREFIX}{match}" if match else None


# Known renamed/legacy pages -> instant, exact redirects (cheapest resolver)
aliases = AliasMappingResolver({
    "schedule-2025": "schedule",
    "old-sponsors": "sponsors",
})

# Typos against the app's real top-level routes (/schedule, /sponsors, ...)
routes = FlaskRoutesResolver()

# Missing/reordered words, wrong case, and bare fragments for /talks/<slug>
talks = TalkSlugResolver(Talk, slug_field="slug", fuzzy_cutoff=0.6)

SelfHeal(app, resolvers=[aliases, routes, talks], redirect_pattern="/{slug}")


# ---------------------------------------------------------------------------
# Shared layout - bigger font + Arial, since this gets projected on a big
# screen during the live demo.
# ---------------------------------------------------------------------------
def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
    body {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 28px;
        line-height: 1.5;
        max-width: 1000px;
        margin: 50px auto;
        padding: 0 30px;
    }}
    a {{ color: #0b63ce; }}
    li {{ margin-bottom: 0.7em; }}
    code {{ background: #f2f2f2; padding: 0.1em 0.4em; border-radius: 4px; }}
    small {{ color: #666; font-size: 0.7em; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


# Each broken demo URL, what's "wrong" with it, and the resolver/technique
# that heals it - shown on the homepage so the audience can see the mapping.
DEMOS = [
    ("/scedule", "typo in a URL segment", "FlaskRoutesResolver"),
    ("/schedule-2025", "renamed/legacy page", "AliasMappingResolver"),
    ("/talks/self-healing-urls", "missing slug words", "TalkSlugResolver (DatabaseResolver)"),
    ("/talks/urls-self-healing", "reordered slug words", "TalkSlugResolver (DatabaseResolver)"),
    ("/talks/Self-Healing-URLs-Explained-Hollis", "wrong case", "TalkSlugResolver (DatabaseResolver)"),
    ("/talks/hollis", "bare fragment, healed end-to-end", "TalkSlugResolver (DatabaseResolver)"),
]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    items = "".join(
        f'<li><a href="{href}"><code>{href}</code></a><br>'
        f'{desc} \u2192 <small>{technique}</small></li>'
        for href, desc, technique in DEMOS
    )
    return page("Self-Healing Demo", f"<h1>Self-Healing Demo</h1><ul>{items}</ul>")


@app.route("/schedule")
def schedule():
    return page("Schedule", "<h1>Schedule</h1><p>Day 1: Keynotes. Day 2: Talks. Day 3: Sprints.</p>")


@app.route("/speakers")
def speakers():
    return page("Speakers", "<h1>Speakers</h1><p>" + ", ".join(t["speaker"] for t in TALKS) + "</p>")


@app.route("/sponsors")
def sponsors():
    return page("Sponsors", "<h1>Sponsors</h1><p>Thanks to everyone who made this event possible!</p>")


@app.route("/contact")
def contact():
    return page("Contact", "<h1>Contact</h1><p>hello@europython2026.example</p>")


@app.route("/talks")
def talks_index():
    items = "".join(
        f'<li><a href="/talks/{t.slug}">{t.title}</a> - {t.speaker}</li>'
        for t in Talk.query.all()
    )
    return page("Talks", f"<h1>Talks</h1><ul>{items}</ul>")


@app.route("/talks/<slug>")
def talk_detail(slug):
    talk = Talk.query.filter_by(slug=slug).first_or_404()
    return page(talk.title, f"<h1>{talk.title}</h1><p>{talk.speaker}</p>")


def seed():
    db.create_all()
    if Talk.query.count() == 0:
        for t in TALKS:
            db.session.add(Talk(**t))
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        seed()
    app.run(debug=True)
