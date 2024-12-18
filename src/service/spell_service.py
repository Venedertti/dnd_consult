import logging
from src.database import db
from flask import current_app
from sqlalchemy.exc import IntegrityError
from src.database.spell_model import Spell
from src.database.classes_model import Classes
from src.database.rel_spell_class_model import RelationalSpellClass

class SpellService:

    def create_spell(data, class_names):
        try:
            spell = Spell(
                name=data['name'],
                level=data['level'],
                school=data['school'],
                casting_time=data['casting_time'],
                range=data['range'],
                components=data['components'],
                duration=data['duration'],
                description=data['description'],
                source=data['source'],
                is_homebrew=data['is_homebrew'],
                is_ritual=data['is_ritual'],
                requires_concentration=data['requires_concentration'],
                image_url=data['image_url'],
                created_by=data['created_by']
            )
            db.session.add(spell)
            db.session.commit()

            spell = Spell.query.filter_by(name=spell.name).first_or_404()
            current_app.logger.info(f"Spell created: ID={spell.id}, Name={spell.name}")
            
            for class_name in class_names:
                spell_class = RelationalSpellClass(spell_id=spell.id, class_name=class_name)
                db.session.add(spell_class)

            db.session.commit()
            return spell

        except IntegrityError as e:
            db.session.rollback()
            raise Exception("Erro ao criar o feitiço ou associar as classes.")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Ocorreu um erro inesperado: {str(e)}")

    @staticmethod
    def get_spells():
        return Spell.query.all()

    @staticmethod
    def get_spell(id):
        return Spell.query.get_or_404(id)

    @staticmethod
    def get_spell_by_name(name):
        return Spell.query.filter_by(name=name).first_or_404()
    
    @staticmethod
    def get_all_spells_by_name(name):
        return Spell.query.filter(Spell.name.ilike(f"%{name}%")).all()
    
    @staticmethod
    def update_spell(id, name, level, school, casting_time, range, components, duration, description, classes, source, is_homebrew, is_ritual, requires_concentration, image_url, created_by):
        spell = Spell.query.get_or_404(id)
        spell.name = name
        spell.level = level
        spell.school = school
        spell.casting_time = casting_time
        spell.range = range
        spell.components = components
        spell.duration = duration
        spell.description = description

        class_instances = []
        for class_name in classes:
            class_instance = Classes.query.filter_by(name=class_name).first()
            if not class_instance:
                raise ValueError(f"Classe '{class_name}' não encontrada.")
            class_instances.append(class_instance)

        spell.classes = class_instances
        spell.source = source
        spell.is_homebrew = is_homebrew
        spell.is_ritual = is_ritual
        spell.requires_concentration = requires_concentration
        spell.image_url = image_url
        spell.created_by = created_by

        db.session.commit()
        return spell

    @staticmethod
    def delete_spell(spell_id):
        spell = Spell.query.get_or_404(spell_id)
        
        spell.classes = []
        db.session.commit()
        
        db.session.delete(spell)
        db.session.commit()

