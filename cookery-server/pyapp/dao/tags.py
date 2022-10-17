from pyapp.dao.base import orm, db
from pyapp.permissions import PermissionStr
from pyapp.dao.entities import RecipeTag

@orm.db_session
def db_tags_get(search_term):
    return list(orm.select(x.rt_tag for x in RecipeTag if search_term in x.rt_tag))

@orm.db_session
def db_get_tag_categories(group):        
    tags = list(orm.select(x.rt_tag for x in RecipeTag if x.rt_recipe.rec_group == group))

    m = set(x.partition(':')[0] for x in tags)
    r = {}
    
    for category in m:    
        tags_of_category = [y.partition(':')[2] for y in tags if y.startswith(category+':')]

        if len(tags_of_category) == 0:
            if '$ungrouped' in r:
                r['$ungrouped'].append(category)
            else:
                r['$ungrouped'] = [category]
        else:
            r[category] = tags_of_category

    return r