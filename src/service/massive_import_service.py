import requests
from src.database import db
from flask import current_app
from src.database.spell_model import Spell
from src.service.import_process_service import ImportProcessService
from src.database.rel_spell_class_model import RelationalSpellClass

class MassiveImportService:
    @staticmethod
    def start_import(process_id, app):
        with app.app_context():
            try:
                ImportProcessService.update_process_status(process_id, 'in_progress')
                MassiveImportService._import_spells_from_dnd5eapi(process_id)
                ImportProcessService.update_process_status(process_id, 'completed', 'Data migration successfully completed')
            except Exception as e:
                ImportProcessService.update_process_status(process_id, 'failed', str(e))
                current_app.logger.error(f'Error during import process {process_id}: {e}')

    @staticmethod
    def _import_spells_from_dnd5eapi(process_id):
        url = 'https://www.dnd5eapi.co/api/spells'
        while url:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f'Failed to fetch spells: {response.status_code}')
            
            data = response.json()
            for spell_detail in data.get('results', []):
                spell_name = spell_detail.get('name')
                if not spell_name:
                    continue

                spell_url = f'https://www.dnd5eapi.co/api/spells/{spell_detail.get('index')}'
                spell_response = requests.get(spell_url)
                if spell_response.status_code != 200:
                    continue

                spell_data = spell_response.json()

                spell = Spell(
                    name=spell_name,
                    level=spell_data.get('level', 0),
                    school=spell_data.get('school', {}).get('name', 'Unknown') if isinstance(spell_data.get('school'), dict) else 'Unknown',
                    casting_time=spell_data.get('casting_time', 'Unknown'),
                    range=spell_data.get('range', 'Unknown'),
                    components=','.join(spell_data.get('components', [])),
                    duration=spell_data.get('duration', 'Unknown'),
                    description=''.join(spell_data.get('desc', [])),
                    source='D&D 5E API',
                    is_homebrew=spell_data.get('homebrew', False),
                    is_ritual=spell_data.get('ritual', False),
                    requires_concentration=spell_data.get('concentration', False),
                    image_url=spell_data.get('image', None),
                    created_by='system'
                )

                try:
                    db.session.add(spell)
                    db.session.commit()
                    
                    classes_data = spell_data.get('classes', [])
                    
                    for class_obj in classes_data:
                        relational_obj= RelationalSpellClass(
                            spell_id= spell.id,
                            class_name= class_obj.get('name')
                        )
                    
                        db.session.add(relational_obj)
                        db.session.commit()
                    
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.error(f'Failed to import spell {spell_name}: {e}')

            url = data.get('next')

        current_app.logger.info(f'Import process {process_id} completed successfully.')
