import urllib
from string import ascii_lowercase, digits
import random

from pony.orm import desc
from pyapp.dao.base import orm
from pyapp.permissions import PermissionStr
from pyapp.dao.entities import Recipe
from pyapp.dao.sorting import RecipeSortOrder
from uuid import UUID

def __generate_random_alphanum_str(length):
    return ''.join([random.choice(ascii_lowercase + digits) for i in range(length)])

def generate_recipe_short_id():
    '''
    Generates a database-unique alphanumeric string of length 8
    '''
    short_id = None
    while not short_id or __db_recipe_short_id_exists(short_id):
        short_id = __generate_random_alphanum_str(8)

    return short_id

def generate_recipe_readable_id(title):
    '''
    Generate a unique readable-id for the given recipe
    '''
    replace_symbols = {
        'ä': 'ae', 'Ä': 'Ae',
        'ö': 'oe', 'Ö': 'oe',
        'ü': 'ue', 'Ü': 'ue',
        'ß': 'ss', 'ẞ': 'SS'
    }

    readable_title = ''
    for c in title:
        if c in replace_symbols:
            readable_title += replace_symbols[c]
        else:
            readable_title += c

    return urllib.parse.quote_plus(readable_title)

@orm.db_session
def db_recipe_by_id(id):
    if isinstance(id, str):
        id = UUID(id)

    return Recipe.get(rec_uid = id)

@orm.db_session
def db_recipe_by_short_id(short_id):
    return Recipe.get(rec_short_id = short_id)

@orm.db_session
def __db_recipes_filter(group, q, ingredients, tags):
    if q:
        query =  Recipe.select(lambda r: r.rec_group == group and q in r.rec_title)
    else:
        query =  Recipe.select(rec_group = group)

    for ingredient_id in ingredients:
        query = query.filter(lambda r: orm.exists(ing for ing in r.rec_ingredients if ing.ri_ingredient.in_uid == UUID(ingredient_id)))

    for tag in tags:
        query = query.filter(lambda r: orm.exists(t for t in r.rec_tags if t.rt_tag == tag))

    return query

    #return  Recipe.select(lambda r: q in r.rec_title)

@orm.db_session
def db_recipes_count(group = '', q = '', ingredients = [], tags = []):
    return __db_recipes_filter(group = group, q = q, ingredients = ingredients, tags = tags).count()

@orm.db_session
def db_recipes_get(group = '', page = 1, per_page = 3, q = '', sortOrder = RecipeSortOrder.latest_first, ingredients = [], tags = []):
    # TODO: sort
    return __db_recipes_filter(group = group, q = q, ingredients = ingredients, tags = tags).order_by(sortOrder.getOrmOrderTerm()).page(page, per_page)

@orm.db_session
def db_recipes_get_latest(group, count):
    return Recipe.select(rec_group = group).order_by(desc(Recipe.rec_created_on)).limit(count)

@orm.db_session
def __db_recipe_short_id_exists(short_id):
    '''
    Return a value which indicates if the given short_id already exists
    in the database
    '''
    return orm.exists(r for r in Recipe if r.rec_short_id == short_id)