from src.database import db

class Classes(db.Model):
    __tablename__ = 'classes'

    name = db.Column(db.String(100), nullable=False, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(255), nullable=False)

    spells = db.relationship(
        'Spell',
        secondary='rel_spell_class',
        back_populates='classes',
        overlaps='classes_,spells_'
    )
