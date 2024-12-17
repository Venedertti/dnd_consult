from src.database import db

class RelationalSpellClass(db.Model):
    __tablename__ = 'relational_spell_class'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spell_id = db.Column('spell_id', db.Integer, db.ForeignKey('spells.id'), nullable=False)
    class_name = db.Column('class_name', db.String(100), db.ForeignKey('classes.name'), nullable=False)

    def __init__(self, spell_id, class_name):
        self.spell_id = spell_id
        self.class_name = class_name