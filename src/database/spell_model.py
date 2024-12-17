# src/database/spell_model.py
from src.database import db
from datetime import datetime, timezone

class Spell(db.Model):
    __tablename__ = 'spells'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    school = db.Column(db.String(100), nullable=False)
    casting_time = db.Column(db.String(100), nullable=False)
    range = db.Column(db.String(100), nullable=False)
    components = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(255), nullable=False)
    is_homebrew = db.Column(db.Boolean, default=False)
    is_ritual = db.Column(db.Boolean, default=False)
    requires_concentration = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(255))
    created_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    classes = db.relationship(
        'Classes',
        secondary='relational_spell_class',
        back_populates='spells',
        overlaps='spells_,classes_',
        cascade="all, delete",
        passive_deletes=True
    )

    def __init__(self, name, level, school, casting_time, range, components, duration, description, source, is_homebrew, is_ritual, requires_concentration, image_url, created_by):
        self.name = name
        self.level = level
        self.school = school
        self.casting_time = casting_time
        self.range = range
        self.components = components
        self.duration = duration
        self.description = description
        self.source = source
        self.is_homebrew = is_homebrew
        self.is_ritual = is_ritual
        self.requires_concentration = requires_concentration
        self.image_url = image_url
        self.created_by = created_by
