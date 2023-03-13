""" Foundational Model of Anatomy (FMA) integration """

import os

from flask import Blueprint, jsonify, request
from owlready2 import (
    default_world,
    get_namespace,
    get_ontology,
)

from kgraphserve.files.download import download

fma = Blueprint('fma', __name__)

owl_path = './data/fma.owl'
url = 'https://data.bioontology.org/ontologies/FMA/submissions/29/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb'

if not os.path.exists(owl_path):
    print('Downloading FMA (this may take a while)...')
    download(url, owl_path)

onto = get_ontology(f'file://{owl_path}').load()
obo = get_namespace('http://purl.org/sig/ont/fma/')


def parse_data(entity_name):
    """
    Parses SPARQL data to generate relations for a particular entity

    :param entity_name: str - The name of the FMA entity
    :return data: dict - Each key is the relation type and each value is a list of related entities
    """

    properties = list(default_world.sparql(f'''
       SELECT ?y
       {{ ?x rdfs:label "{entity_name}" .
         ?x rdfs:subClassOf* ?y }}
    '''))

    data = {
        'name': entity_name,
        'arterial_supply': [],
        'children': [],
        'parents': [],
        'receives_input_from': [],
        'sends_output_to': [],
    }

    for p in properties:

        p = p[0]

        if str(p).startswith('fma.receives_input_from'):
            value = p.__dict__['value']
            label = getattr(obo, str(value)[4:]).label[0]
            data['receives_input_from'].append(label)

        elif str(p).startswith('fma.sends_output_to'):
            value = p.__dict__['value']
            label = getattr(obo, str(value)[4:]).label[0]
            data['sends_output_to'].append(label)

        elif str(p).startswith('fma.arterial_supply'):
            value = p.__dict__['value']
            label = getattr(obo, str(value)[4:]).label[0]
            data['arterial_supply'].append(label)

        elif str(p).startswith('fma.regional_part_of'):
            value = p.__dict__['value']
            label = getattr(obo, str(value)[4:]).label[0]
            data['parents'].append(label)

        elif str(p).startswith('fma.regional_part'):
            value = p.__dict__['value']
            label = getattr(obo, str(value)[4:]).label[0]
            child = parse_data(label)
            data['children'].append(child)

    data['arterial_supply'].sort()
    data['parents'].sort()
    data['receives_input_from'].sort()
    data['sends_output_to'].sort()

    data['children'] = sorted(data['children'], key=lambda d: d['name'])

    return data


@fma.route('/fma/get_data', methods=['POST'])
def get_data():
    """ Returns relations for a given entity from the FMA """

    entity_name = request.json.get('entity_name')
    data = parse_data(entity_name)
    response = jsonify(data)

    return response
