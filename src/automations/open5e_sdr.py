import requests
from src.database import db
from src.database.spell_model import Spell
from flask import current_app

def import_massive():
    '''
    Import spells from the D&D 5e API and save them to the database.
    Fields not provided by the API will be defaulted as follows:
      - Text fields: Default to the spell name.
      - Boolean fields: Default to False.
    '''
    url = 'https://www.dnd5eapi.co/api/spells'
    headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = ''
        spells_data = response.json()
        spells = spells_data['results']

        with current_app.app_context():
            for spell_data in spells:
                try:
                    # Fetch detailed spell data
                    spell_detail_response = requests.get(f'https://www.dnd5eapi.co{spell_data["url"]}', headers=headers)
                    if spell_detail_response.status_code != 200:
                        raise Exception(f'Failed to fetch details for {spell_data["name"]}')

                    spell_detail = spell_detail_response.json()

                    # Normalize data
                    spell_name = spell_detail.get('name', 'Unknown Spell')
                    spell = Spell(
                        name=spell_name,
                        level=spell_detail.get('level', 0),
                        school=spell_detail.get('school', {}).get('name', spell_name),
                        casting_time=spell_detail.get('casting_time', spell_name),
                        range=spell_detail.get('range', spell_name),
                        components=', '.join(spell_detail.get('components', [])),
                        duration=spell_detail.get('duration', spell_name),
                        description=spell_detail.get('desc', [spell_name])[0],
                        classes=', '.join([cls['name'] for cls in spell_detail.get('classes', [])]),
                        source='Open5E SDR',
                        is_homebrew=False,
                        is_ritual=spell_detail.get('ritual', False),
                        requires_concentration=spell_detail.get('concentration', False),
                        image_url=None,
                        created_by='system'
                    )

                    # Add spell to the database session
                    db.session.add(spell)
                    result += f'Added spell: {spell_name}\n'
                    print(f'Added spell: {spell_name}')

                except Exception as e:
                    # If an error occurs, capture the spell name and the error message
                    result += f'Error with spell {spell_data["name"]}: {str(e)}\n'
                    print(f'Error with spell {spell_data["name"]}: {str(e)}')

            # Commit the transaction
            db.session.commit()
            print('All spells have been successfully imported!')
            print('Results:', result)  # Optionally print the result string with all errors and successes
    else:
        print(f'Failed to fetch spells. HTTP Status Code: {response.status_code}')
