from flask_restx import Namespace, Resource, fields
from datetime import datetime

def __get_fields_type(field_definition):
    if isinstance(field_definition, fields.String):
        return str
    
    if isinstance(field_definition, fields.List):
        return list

    if isinstance(field_definition, fields.Integer):
        return int    

    if isinstance(field_definition, fields.Float):
        return float

    raise Exception(f"parserForModel: Unsupported field definition {field_definition}")

def parserForModel(api, model, location):
    '''
    Generates a flask-restplus parser for the given model
    '''

    parser = api.parser()

    for field in model:
        definition = model[field]
        
        description = None
        if hasattr(definition, 'description') and definition.description is not None:
            description = definition.description
        
        choices = None
        if hasattr(definition, 'enum') and definition.enum is not None:
            choices = definition.enum
        
        default = None
        if hasattr(definition, 'default') and definition.default is not None:
            default = definition.default

        parser.add_argument(field, required=definition.required, type=__get_fields_type(definition), help=description, location=location, default=default, choices=choices)

    return parser