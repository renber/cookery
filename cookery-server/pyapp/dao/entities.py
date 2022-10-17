from enum import Enum
from datetime import datetime, timedelta
from pyapp.dao.base import db, orm, tablename
from uuid import UUID
from pyapp import config

import re

class User(db.Entity):
    _table_ = tablename('USER')

    usr_uid = orm.PrimaryKey(UUID, auto=True)
    usr_active = orm.Required(bool, default=False)
    usr_email = orm.Required(str)
    usr_name = orm.Required(str)
    usr_password = orm.Required(bytes)
    usr_roleid = orm.Optional(str, nullable=True)
    usr_isadmin = orm.Optional(bool)

class Role(db.Entity):
    _table_ = tablename('ROLES')

    rl_uid = orm.PrimaryKey(UUID, auto=True)
    rl_name = orm.Required(str)
    rl_comment = orm.Optional(str, nullable=True)

class Permission(db.Entity):
    _table_ = tablename('PERMISSIONS')

    perm_role_uid = orm.Required(UUID) # add relationship to Role
    perm_granted = orm.Required(str)

    orm.PrimaryKey(perm_role_uid, perm_granted)

class Session(db.Entity):
    _table_ = tablename('SESSIONS')

    ses_uid = orm.PrimaryKey(UUID, auto=True)
    ses_userid = orm.Required(UUID)
    ses_expires = orm.Required(datetime)

    _defaultSessionLifetime = timedelta(minutes=10)

class IngredientGroup(db.Entity):
    _table_ = tablename('INGREDIENT_GROUPS')

    ig_uid = orm.PrimaryKey(UUID, auto=True)
    ig_parent_group = orm.Optional("IngredientGroup", column='IG_PARENT_GROUP_UID', nullable=True, reverse='ig_child_groups')
    ig_child_groups = orm.Set("IngredientGroup", reverse='ig_parent_group')
    ig_name = orm.Required(str)
    ig_image_id = orm.Optional(str, nullable=True)

    ig_ingredients = orm.Set("Ingredient", reverse="in_group")

    @property
    def uid_str(self):
        return str(self.ig_uid)

    @property
    def has_child_groups(self):
        return len(self.ig_child_groups) > 0

    @property
    def has_ingredients(self):
        return len(self.ig_ingredients) > 0

    @property
    def path(self):
        if self.ig_parent_group:
            return self.ig_parent_group.path + ' >> ' + self.ig_name
        else:
            return self.ig_name

class Ingredient(db.Entity):
    _table_ = tablename('INGREDIENTS')

    in_uid = orm.PrimaryKey(UUID, auto=True)
    in_group = orm.Required(IngredientGroup, column='IN_GROUP_UID', nullable=True, reverse='ig_ingredients')
    in_name = orm.Required(str)
    in_singular = orm.Optional(str)
    in_image_id = orm.Optional(str, nullable=True)

    in_associated_recipe = orm.Optional('Recipe', column='IN_RECIPE_UID', nullable=True, reverse='rec_recipe_for_ingredient')

    # needed by Pony
    in_used_in_recipes = orm.Set("RecipeIngredient", reverse="ri_ingredient")

    @property
    def uid_str(self):
        return str(self.in_uid)

    @property
    def path(self):
        if self.in_group:
            return self.in_group.path
        else:
            return ''

    @property
    def associated_recipe_url(self):
        # resolve associated recipe urls, if any    
        if self.in_associated_recipe != None:
            recipe = self.in_associated_recipe
            return f'/{recipe.rec_group}/{recipe.rec_short_id}/{recipe.rec_readable_id}'
        return None

class Recipe(db.Entity):
    _table_ = tablename('RECIPES')

    rec_uid = orm.PrimaryKey(UUID, auto=True)
    rec_short_id = orm.Required(str)
    rec_readable_id = orm.Required(str)
    rec_group = orm.Required(str)
    rec_title = orm.Required(str)
    rec_preparation = orm.Required(orm.LongUnicode)
    rec_created_on = orm.Required(datetime)    
    rec_comments = orm.Optional(str)

    rec_portion_size = orm.Required(float)
    rec_portion_text = orm.Required(str)

    rec_ingredients = orm.Set("RecipeIngredient", reverse="ri_recipe")
    rec_tags = orm.Set("RecipeTag", reverse="rt_recipe")

    rec_recipe_for_ingredient = orm.Optional('Ingredient', reverse='in_associated_recipe')

    @property
    def uid_str(self):
        return str(self.rec_uid)

    def get_steps(self):
        # steps are separated by blank lines in preparation
        # greedily match 2 or more new-lines
        blank_line_regex = r"(?:\r?\n){2,}"
        return re.split(blank_line_regex, self.rec_preparation.strip())

class RecipeIngredient(db.Entity):
    '''
    An ingredient which is used in a recipe (including quantity)
    '''
    _table_ = tablename('RECIPE_INGREDIENTS')

    ri_id = orm.PrimaryKey(int, auto=True)
    ri_recipe = orm.Required(Recipe, column='RI_RECIPE_UID', reverse='rec_ingredients')
    ri_position = orm.Required(int)
    # if this is NULL, then the entity represents a caption (title = ri_comment)
    ri_ingredient = orm.Optional(Ingredient, column='RI_INGREDIENT_UID', reverse='in_used_in_recipes')
    ri_quantity = orm.Optional(float, nullable=True)
    ri_unit = orm.Optional(str)
    ri_comment = orm.Optional(str)

    @property
    def is_caption(self):
        return self.ri_ingredient == None

    @property
    def caption(self):
        return self.ri_comment if self.is_caption else ''

class RecipeTag(db.Entity):
    '''
    A tag which has been assigned to a recipe
    '''
    _table_ = tablename('RECIPE_TAGS')

    rt_recipe = orm.Required(Recipe, column='RT_RECIPE_UID', reverse='rec_tags')
    rt_tag = orm.Required(str)

    orm.PrimaryKey(rt_recipe, rt_tag)

#
# helper entities
# mapping classes without corresponding tables
#

class StatCount(db.Entity):
    '''
    Class for statistical queries
    '''
    entity_id = orm.PrimaryKey(str)
    entity_name = orm.Optional(str)
    stat_count = orm.Required(int)