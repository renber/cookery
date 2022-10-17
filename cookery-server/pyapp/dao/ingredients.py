from pyapp.dao.base import orm
from pyapp.permissions import PermissionStr
from pyapp.dao.entities import Ingredient, IngredientGroup

@orm.db_session
def db_ingredients_get_top_level_groups():
    return orm.select(ig for ig in IngredientGroup if ig.ig_parent_group is None).order_by(IngredientGroup.ig_name)[:]

@orm.db_session
def db_ingredients_get_group(group_uid):
    return IngredientGroup.get(ig_uid=group_uid)

@orm.db_session
def db_ingredient_get(ingredient_uid):
    return Ingredient.get(in_uid=ingredient_uid)

@orm.db_session
def db_ingredients_search(searchText):
    return list(orm.select(ing for ing in Ingredient if searchText in ing.in_name).order_by(Ingredient.in_name)[:])