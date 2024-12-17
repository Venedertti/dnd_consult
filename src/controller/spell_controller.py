from src.automations import open5e_sdr
from flask import Blueprint, request, jsonify
from src.service.spell_service import SpellService
from src.service.classes_service import ClassesService

spell_bp = Blueprint('spell', __name__)

@spell_bp.route('/create', methods=['POST'])
def create_spell():
    data = request.get_json()
    class_names = request.json.get('classes')

    if not class_names:
        return jsonify({'error': 'As classes são obrigatórias.'}), 400

    class_objects = ClassesService.get_classes_by_names(class_names)
    
    if len(class_objects) != len(class_names):
        missing_classes = set(class_names) - {cls.name for cls in class_objects}
        return jsonify({'error': f'Classes não encontradas: {', '.join(missing_classes)}'}), 400

    class_names = [cls.name for cls in class_objects]

    try:
        spell= SpellService.create_spell(data= data, class_names= class_names)
        return jsonify({
    'message': 'Spell created with id: {}'.format(str(spell.id))
}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@spell_bp.route('/automate/', methods=['POST'])
def bulkImportOpen5eSDR():
    source= data['source']
    data= request.get_json()
    
    result= ''
    if source == 'Open5E SDR':
        result = open5e_sdr.import_massive()
    
    return jsonify({'logs':result}), 200

@spell_bp.route('/getAll', methods=['GET'])
def get_spells():
    spells = SpellService.get_spells()
    return jsonify([{
        'id': spell.id,
        'name': spell.name,
        'level': spell.level,
        'school': spell.school
    } for spell in spells])

@spell_bp.route('/get/<int:id>', methods=['GET'])
def get_spell(id):
    spell = SpellService.get_spell(id)
    
    classes_data = [
        {
            'name': c.name,
            'type': c.type,
            'source': c.source
        }
        for c in spell.classes
    ]
    
    return jsonify({
        'id': spell.id,
        'name': spell.name,
        'level': spell.level,
        'school': spell.school,
        'castingTime': spell.casting_time,
        'range': spell.range,
        'components': spell.components,
        'duration': spell.duration,
        'description': spell.description,
        'classes': classes_data,
        'source': spell.source,
        'isHomebrew': spell.is_homebrew,
        'isRitual': spell.is_ritual,
        'requiresConcentration': spell.requires_concentration,
        'imageUrl': spell.image_url,
        'createdBy': spell.created_by,
        'createdAt': spell.created_at
    })

@spell_bp.route('/findAllByName', methods=['GET'])
def find_all_spells_by_name():
    name = request.args.get('name')
    
    if not name:
        return jsonify({'error': 'The "name" parameter is required.'}), 400
    
    try:
        spells = SpellService.get_all_spells_by_name(name)
        
        if not spells:
            return jsonify({'message': 'No spells found with that name.'}), 404
        
        spells_data = []
        for spell in spells:
            classes_data = [
                {'name': c.name, 'type': c.type, 'source': c.source} 
                for c in spell.classes
            ]
            spells_data.append({
                'id': spell.id,
                'name': spell.name,
                'level': spell.level,
                'school': spell.school,
                'castingTime': spell.casting_time,
                'range': spell.range,
                'components': spell.components,
                'duration': spell.duration,
                'description': spell.description,
                'classes': classes_data,
                'source': spell.source,
                'isHomebrew': spell.is_homebrew,
                'isRitual': spell.is_ritual,
                'requiresConcentration': spell.requires_concentration,
                'imageUrl': spell.image_url,
                'createdBy': spell.created_by,
                'createdAt': spell.created_at
            })
        
        return jsonify(spells_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@spell_bp.route('/update/<int:id>', methods=['PUT'])
def update_spell(id):
    data = request.get_json()
    class_names = data.pop('classes', [])

    try:
        updated_spell = SpellService.update_spell(id, classes=class_names, **data)
        return jsonify({
            'id': updated_spell.id,
            'name': updated_spell.name,
            'level': updated_spell.level,
            'school': updated_spell.school,
            'casting_time': updated_spell.casting_time,
            'range': updated_spell.range,
            'components': updated_spell.components,
            'duration': updated_spell.duration,
            'description': updated_spell.description,
            'classes': [{'name': c.name, 'type': c.type, 'source': c.source} for c in updated_spell.classes],
            'source': updated_spell.source,
            'is_homebrew': updated_spell.is_homebrew,
            'is_ritual': updated_spell.is_ritual,
            'requires_concentration': updated_spell.requires_concentration,
            'image_url': updated_spell.image_url,
            'created_by': updated_spell.created_by
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@spell_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_spell(id):
    SpellService.delete_spell(id)
    return jsonify({'message': 'Spell deleted'}), 204
