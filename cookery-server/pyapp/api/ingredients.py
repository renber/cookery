import logging
import re

from flask import request, send_from_directory, abort
from flask_restx import Namespace, Resource, fields
import bcrypt
from pyapp import config
from pyapp.auth import auth, parseAuthHeader
from pyapp.permissions import PermissionStr
from pyapp.session import sessionMgr, TokenStatus, getCurrentSession
from pyapp.dao.base import orm
from pyapp.dao.entities import Ingredient, IngredientGroup
from pyapp.dao.ingredients import db_ingredient_get, db_ingredients_get_top_level_groups, db_ingredients_get_group, db_ingredients_search
from pyapp.api.utils import parserForModel

logger = logging.getLogger(__name__)

api = Namespace('ingredients', description='Access to ingredients')

ingredient_model = api.model('Ingredient', {
    'id': fields.String(attribute='uid_str'),
    'group_id': fields.String(attribute='in_group.uid_str'),
    'name': fields.String(attribute='in_name'),
    'singular': fields.String(attribute='in_singular'),    
    'associated_recipe_id': fields.String(attribute='in_associated_recipe.uid_str'),
    'associated_recipe_url': fields.String(attribute='associated_recipe_url'),
    'path': fields.String(attribute='path')
})

new_ingredient_model = api.model('NewIngredient', {
    'group_id': fields.String(),
    'name': fields.String(),
    'associated_recipe_id': fields.String(required = False),
    'singular': fields.String()
})

new_ingredient_model_parser = parserForModel(api, new_ingredient_model, 'json')

ingredient_child_group_model = api.model('IngredientSubGroupInfo', {
    'id': fields.String(attribute='uid_str'),
    'name': fields.String(attribute='ig_name'),
    'has_ingredients': fields.Boolean(attribute='has_ingredients'),
    'has_child_groups': fields.Boolean(attribute='has_child_groups')
})

ingredient_group_model = api.model('IngredientGroupInfo', {
    'id': fields.String(attribute='uid_str'),
    'name': fields.String(attribute='ig_name'),
    'ingredients': fields.List(fields.Nested(ingredient_model), attribute="ingredients_list"),
    'child_groups': fields.List(fields.Nested(ingredient_child_group_model), attribute='child_group_list')
})

new_ingredient_group_model = api.model('NewIngredientGroup', {
    'parent_group_id': fields.String(required = False),
    'name': fields.String(required = True),
})

new_ingredient_group_model_parser = parserForModel(api, new_ingredient_group_model, 'json')

query_parser = api.parser()
query_parser.add_argument('q', type=str, required=True, location='args', help='Query text to filter for (min. length = 2)')

def transform_group_for_model(group):
    # the pony orm 1:n fields are of type set, we have to transform them to a list to be able to marshal them using fields.List
    group.ingredients_list = list(group.ig_ingredients)
    group.ingredients_list.sort(key=lambda x: x.in_name)
    group.child_group_list = list(group.ig_child_groups)
    group.child_group_list.sort(key=lambda x: x.ig_name)
    return group

@api.route("/<ingredient_id>")
class Ingredients(Resource):
    '''
    Access the ingredient with the given id
    '''

    @api.require_permissions(PermissionStr.INGREDIENT_READ)
    @orm.db_session
    @api.marshal_with(ingredient_model)
    def get(self, ingredient_id):
        ing = db_ingredient_get(ingredient_id)
        if not ing:
            abort(404)

        return ing

    @api.require_permissions(PermissionStr.INGREDIENT_WRITE)
    @orm.db_session
    @api.expect(new_ingredient_model)
    @api.marshal_with(ingredient_model)    
    def post(self, ingredient_id):
        '''
        Update data of the ingredient with the given id
        '''
        ing = db_ingredient_get(ingredient_id)
        if not ing:
            abort(404)

        args = new_ingredient_model_parser.parse_args()

        ing.in_name = args.name
        ing.in_singular = args.singular
        

@api.route('')
class AllIngredient(Resource):

    @api.require_permissions(PermissionStr.INGREDIENT_READ)
    @orm.db_session
    @api.expect(query_parser)
    @api.marshal_list_with(ingredient_model)
    def get(self):
        '''
        Retrieve the list of available ingredients which match the given search term
        '''
        args = query_parser.parse_args()

        if args.q and len(args.q) > 1:
            db_list = db_ingredients_search(args.q)
        else:
            db_list = []

        return db_list

    '''
    Access a ingredients
    '''
    @api.require_permissions(PermissionStr.INGREDIENT_WRITE)
    @orm.db_session
    @api.expect(new_ingredient_model)
    @api.marshal_with(ingredient_model)
    def put(self):
        '''
        Create a new ingredient with the given properties
        '''
        args = new_ingredient_model_parser.parse_args()

        parent_group = db_ingredients_get_group(args.group_id)
        if not parent_group:
            abort(400, 'Group does not exist')

        new_ing = Ingredient(in_name = args.name, in_singular = args.singular, in_group = parent_group)

        new_ing.flush()
        return new_ing

@api.route("/groups")
class IngredientTopLevelGroups(Resource):
    '''
    Return the top-level ingredient groups
    '''

    @api.require_permissions(PermissionStr.INGREDIENT_READ)
    @orm.db_session
    @api.marshal_list_with(ingredient_child_group_model)
    def get(self):
        rlist = list(db_ingredients_get_top_level_groups())
        return rlist

    @api.require_permissions(PermissionStr.INGREDIENT_WRITE)
    @orm.db_session
    @api.expect(new_ingredient_group_model)
    @api.marshal_with(ingredient_group_model)
    def put(self):
        '''
        Create a new ingredient group with the given properties
        '''
        args = new_ingredient_group_model_parser.parse_args()

        if args.parent_group_id and len(args.parent_group_id) > 0:
            parent_group = db_ingredients_get_group(args.parent_group_id)
            if not parent_group:
                abort(400, 'Parent group does not exist')

            new_group = IngredientGroup(ig_name = args.name, ig_parent_group = parent_group)
        else:
            new_group = IngredientGroup(ig_name = args.name)

        new_group.flush()
        return transform_group_for_model(new_group)

@api.route("/groups/<group_id>")
class IngredientGroups(Resource):

    @api.require_permissions(PermissionStr.INGREDIENT_READ)
    @orm.db_session
    @api.marshal_with(ingredient_group_model)
    def get(self, group_id):
        '''
        Return information and sub-groups for the specified ingredient group
        '''
        group = db_ingredients_get_group(group_id)
        if group is None:
            abort(404)

        return transform_group_for_model(group)
