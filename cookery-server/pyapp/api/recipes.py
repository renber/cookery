import logging
import re

from pony.orm import commit

from flask import request, send_from_directory, abort
from flask_restx import Namespace, Resource, fields
from enum import Enum
from pyapp import config
from pyapp.storage.ImageStore import imageStore
from pyapp.auth import auth, parseAuthHeader
from pyapp.permissions import PermissionStr
from pyapp.session import sessionMgr, TokenStatus, getCurrentSession
from pyapp.dao.base import orm
from pyapp.dao.entities import Recipe, Ingredient, RecipeIngredient, RecipeTag
from pyapp.dao.recipes import db_recipes_get, db_recipes_count, db_recipes_get_latest, db_recipe_by_short_id, db_recipe_by_id, generate_recipe_short_id, generate_recipe_readable_id
from pyapp.dao.ingredients import db_ingredient_get
from pyapp.api.utils import parserForModel
from pyapp.api.ingredients import ingredient_model
from pyapp.dao.sorting import RecipeSortOrder
import werkzeug
from datetime import datetime

logger = logging.getLogger(__name__)

api = Namespace('recipes', description='Access to recipes')   

recipe_list_latest_model = api.model('RecipeListLatest', {
    'group': fields.String(),
    'count': fields.Integer()
})

recipe_search_model = api.model('RecipeSearch', {
    'group': fields.String(),
    'page': fields.Integer(required = False, descripton = 'Result page number', default = '1'),
    'perPage': fields.Integer(required = False, description = 'Number of elements to return per page', default = 10),
    'sortOrder': fields.String(required = False, description = "Sort order of the result list", default = RecipeSortOrder.latest_first._value_, enum=RecipeSortOrder._member_names_),
    'q': fields.String(required = False),
    'ingredients': fields.String(required = False),
    'tags': fields.String(required = False)
})

recipe_info_model = api.model('RecipeInfo', {
    'id': fields.String(attribute='uid_str'),
    'short_id': fields.String(attribute='rec_short_id'),
    'readable_id': fields.String(attribute='rec_readable_id'),
    'group': fields.String(attribute='rec_group'),
    'title': fields.String(attribute='rec_title'),
    'tags': fields.List(fields.String, attribute='tags_list'),    
    'image_url': fields.String()
})

recipe_list = api.model('RecipeList', {
    'page': fields.Integer,
    'recipe_count': fields.Integer,
    'recipes': fields.Nested(recipe_info_model)
})

recipe_ingredient_full_model = api.model('RecipeIngredientFull', {
    'is_caption': fields.Boolean(required = True, attribute = 'is_caption'),    

    'quantity': fields.Float(attribute='ri_quantity'),
    'unit': fields.String(attribute='ri_unit'),
    'ingredient': fields.Nested(ingredient_model, attribute='ri_ingredient'),
    'comment': fields.String(attribute='ri_comment'),    
})

recipe_model = api.model('Recipe', {
    'id': fields.String(attribute='uid_str'),
    'short_id': fields.String(attribute='rec_short_id'),
    'readable_id': fields.String(attribute='rec_readable_id'),
    'group': fields.String(attribute='rec_group'),
    'title': fields.String(attribute='rec_title'),
    'portion_size': fields.Float(attribute='rec_portion_size'),
    'portion_text': fields.String(attribute='rec_portion_text'),
    'ingredients': fields.List(fields.Nested(recipe_ingredient_full_model), attribute='ingredients_list'),
    'steps': fields.List(fields.String, attribute='steps'),
    'tags': fields.List(fields.String, attribute='tags_list'),
    'comments': fields.String(attribute='rec_comments'),
    'image_url': fields.String()
})

recipe_ingredient_model = api.model('RecipeIngredient', {
    'is_caption': fields.Boolean(required = True), 
    'quantity': fields.Float(required=False),
    'unit': fields.String(required=False),
    'ingredient_id': fields.String(required=True),
    'comment': fields.String(required=False)
})

new_recipe_model = api.model('NewRecipe', {
    'title': fields.String(),
    'group': fields.String(),
    'portion_size': fields.Float(),
    'portion_text': fields.String(),
    'ingredients': fields.List(fields.Nested(recipe_ingredient_model)),    
    'steps': fields.List(fields.String),
    'tags': fields.List(fields.String),
    'comments': fields.String()
})

update_recipe_model = api.model('UpdateRecipe', {
    'title': fields.String(required = False),
    'portion_size': fields.Float(required = False),
    'portion_text': fields.String(required = False),
    'ingredients': fields.List(fields.Nested(recipe_ingredient_model), required = False),
    'steps': fields.List(fields.String, required = False),
    'tags': fields.List(fields.String, required = False),
    'comments': fields.String(required = False)
})


recipe_list_latest_parser = parserForModel(api, recipe_list_latest_model, 'args')
recipe_search_parser = parserForModel(api, recipe_search_model, 'args')

new_recipe_model_parser = parserForModel(api, new_recipe_model, 'json')
update_recipe_model_parser = parserForModel(api, update_recipe_model, 'json')

imageFileParser = api.parser()
imageFileParser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files', required=True)

def transform_recipe_for_model(recipe):
    # the pony orm 1:n fields are of type set, we have to transform them to a list to be able to marshal them using fields.List
    # additionally we restore teh correct order by sorting by the position field
    recipe.ingredients_list = sorted(list(recipe.rec_ingredients), key = lambda x: x.ri_position)    
    recipe.tags_list = sorted(list(r.rt_tag for r in recipe.rec_tags))
    return recipe

@api.route("")
class Recipes(Resource):

    @api.require_permissions(PermissionStr.RECIPE_READ)
    @orm.db_session
    @api.expect(recipe_search_parser)
    @api.marshal_with(recipe_list)
    def get(self):
        '''
        Return a filtered, paged list of recipes of this server
        '''
        args = recipe_search_parser.parse_args()

        if not args.page:
            args.page = 1

        if not args.q:
            args.q = ''

        if not args.sortOrder:
            args.sortOrder = RecipeSortOrder.latest_first
        else:
            args.sortOrder = RecipeSortOrder(args.sortOrder)

        if not args.ingredients:
            args.ingredients = ''

        if not args.tags:
            args.tags = ''

        ingredient_list = list(filter(None, args.ingredients.split(';')))
        tag_list = list(filter(None, args.tags.split(';')))

        rcount = db_recipes_count(group = args.group, q = args.q, ingredients = ingredient_list, tags = tag_list)
        rlist = list(db_recipes_get(group = args.group, page = args.page, per_page = args.perPage, q = args.q, sortOrder=args.sortOrder, ingredients = ingredient_list, tags = tag_list))

        for r in rlist:
            if imageStore.recipe_has_image(r.uid_str):
                r.image_url = f'{config.BASE_URL}/api/v1/recipes/{r.uid_str}/image'
            else:
                r.image_url = None

            # prepare the tags list for marshalling
            r.tags_list = sorted(list(r.rt_tag for r in r.rec_tags))

        return {
            'page': 1,
            'recipe_count': rcount,
            'recipes': rlist
        }

    @api.require_permissions(PermissionStr.RECIPE_WRITE)
    @orm.db_session
    @api.expect(new_recipe_model)
    @api.marshal_with(recipe_info_model)
    def put(self):
        '''
        Create a new recipe
        '''
        args = new_recipe_model_parser.parse_args()
        preparation = "\n\n".join(args.steps)

        recipe = Recipe(rec_short_id = generate_recipe_short_id(), rec_readable_id = generate_recipe_readable_id(args.title), rec_title = args.title, rec_portion_size = args.portion_size, rec_portion_text = args.portion_text, rec_group = args.group, rec_preparation = preparation, rec_comments = args.comments, rec_created_on = datetime.now())

        pos = 0
        for ing in args.ingredients:
            if ing['is_caption']:
                recipe.rec_ingredients.create(ri_position = pos, ri_quantity = 0, ri_unit = '', ri_ingredient = None, ri_comment = ing['comment'])
            else:
                ingredient = db_ingredient_get(ing['ingredient_id'])
                if not ingredient:
                    abort(400, f"Ingredient with ID {ing['ingredient_id']} does not exist")

                qty = ing.get('quantity', None)
                if qty == '':
                    qty = None

                recipe.rec_ingredients.create(ri_position = pos, ri_quantity = qty, ri_unit = ing['unit'], ri_ingredient = ingredient, ri_comment = ing['comment'])

            pos += 1

        if hasattr(args, 'tags'):            
            for a in args.tags:
                recipe.rec_tags.create(rt_tag = a)

        return recipe

@api.route("/latest")
class LatestRecipes(Resource):
    '''
    Return the latest additions from the recipe pool
    '''

    @orm.db_session    
    @api.require_permissions(PermissionStr.RECIPE_READ)
    @api.expect(recipe_list_latest_parser)
    @api.marshal_list_with(recipe_info_model)
    def get(self):
        '''
        Return the 5 most recently added recipes
        '''
        args = recipe_list_latest_parser.parse_args()

        rlist = list(db_recipes_get_latest(args.group, args.count))
        for r in rlist:
            if imageStore.recipe_has_image(r.uid_str):
                r.image_url = f'{config.BASE_URL}/api/v1/recipes/{r.uid_str}/image'
            else:
                r.image_url = None

            # prepare the tags list for marshalling
            r.tags_list = sorted(list(r.rt_tag for r in r.rec_tags))

        return rlist

@api.route("/<recipe_id>")
class RecipeDetail(Resource):

    @api.require_permissions(PermissionStr.RECIPE_READ)
    @orm.db_session
    @api.marshal_list_with(recipe_model)
    def get(self, recipe_id):
        '''
        Return the recipe with the given id or short id
        '''
        recipe = None

        if len(recipe_id) == 8:
            recipe = db_recipe_by_short_id(recipe_id)
        elif len(recipe_id) == 36:
            recipe = db_recipe_by_id(recipe_id)

        if not recipe:
            abort(404)

        recipe.steps = recipe.get_steps()

        if imageStore.recipe_has_image(recipe.uid_str):
            recipe.image_url = f'{config.BASE_URL}/api/v1/recipes/{recipe.uid_str}/image'
        else:
            recipe.image_url = None

        return transform_recipe_for_model(recipe)

    @api.require_permissions(PermissionStr.RECIPE_WRITE)
    @orm.db_session
    @api.expect(update_recipe_model)
    def post(self, recipe_id):
        '''
        Update the recipe with the given id or short id
        '''
        recipe = None

        if len(recipe_id) == 8:
            recipe = db_recipe_by_short_id(recipe_id)
        elif len(recipe_id) == 36:
            recipe = db_recipe_by_id(recipe_id)

        if not recipe:
            abort(404)

        args = update_recipe_model_parser.parse_args()

        if hasattr(args, 'title'):
            recipe.rec_title = args.title
            recipe.rec_readable_id = generate_recipe_readable_id(args.title)

        if hasattr(args, 'steps'):
            preparation = "\n\n".join(args.steps)
            recipe.rec_preparation = preparation

        if hasattr(args, 'comments'):
            recipe.rec_comments = args.comments

        if hasattr(args, 'portion_size'):
            recipe.rec_portion_size = args.portion_size
        
        if hasattr(args, 'portion_text'):
            recipe.rec_portion_text = args.portion_text

        if hasattr(args, 'ingredients'):
            recipe.rec_ingredients.clear()

            pos = 0
            for ing in args.ingredients:
                print(ing)
                if ing['is_caption']:
                    rec_ing = RecipeIngredient(ri_position = pos, ri_recipe = recipe, ri_quantity = 0, ri_unit = '', ri_ingredient = None, ri_comment = ing['comment'])
                else:
                    ingredient = db_ingredient_get(ing['ingredient_id'])
                    if not ingredient:
                        abort(400, f"Ingredient with ID {ing['ingredient_id']} does not exist")

                    qty = ing.get('quantity', None)
                    if qty == '':
                        qty = None

                    rec_ing = RecipeIngredient(ri_position = pos, ri_recipe = recipe, ri_quantity = qty, ri_unit = ing['unit'], ri_ingredient = ingredient, ri_comment = ing['comment'])
                
                recipe.rec_ingredients.add(rec_ing)
                pos += 1

        if hasattr(args, 'tags'):

            updated_tags = set(args.tags)
            existing_tags = set(x.rt_tag for x in recipe.rec_tags)

            toRemove = existing_tags.difference(updated_tags)
            for r in toRemove:
                rem = next((e for e in recipe.rec_tags if e.rt_tag == r), None)
                if rem:
                    recipe.rec_tags.remove(rem)

            toAdd = updated_tags.difference(existing_tags)
            for a in toAdd:
                recipe.rec_tags.create(rt_tag = a)


        return "Successfully updated", 200


@api.route("/<recipe_id>/image")
class RecipeImage(Resource):

    # images do not require permissions (atm) since they could not be used in browser img tags otherwise
    # two possible solutions: - use generated links tied to session ; - pass session token as url query param
    @api.produces(["image/jpg"])
    def get(self, recipe_id):
        '''
        Return the main image for the recipe with the given id
        if it exists
        '''

        recipe = None

        if len(recipe_id) == 8:
            recipe = db_recipe_by_short_id(recipe_id)
        elif len(recipe_id) == 36:
            recipe = db_recipe_by_id(recipe_id)

        # todo: parameters for target size
        try:
            return send_from_directory(config.IMAGE_STORE_FOLDER, filename=f'{str(recipe.rec_uid)}.jpg', mimetype='image/jpeg')
        except FileNotFoundError:
            abort(404)

    @api.require_permissions(PermissionStr.RECIPE_WRITE)
    @api.expect(imageFileParser)
    def post(self, recipe_id):
        '''
        Upload an image and set it as main image of the recipe with the given id
        '''
        recipe = None

        if len(recipe_id) == 8:
            recipe = db_recipe_by_short_id(recipe_id)
        elif len(recipe_id) == 36:
            recipe = db_recipe_by_id(recipe_id)

        if not recipe:
            abort(404)

        args = imageFileParser.parse_args()

        stream = args['image'].stream
        imageStore.update(str(recipe.rec_uid), stream)