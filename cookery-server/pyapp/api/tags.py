import logging
from flask_restx import Namespace, Resource, fields
from pyapp.dao.tags import db_tags_get, db_get_tag_categories
from pyapp.permissions import PermissionStr
from pyapp.api.utils import parserForModel

logger = logging.getLogger(__name__)

api = Namespace('tags', description='Access to tags')

tag_search_model = api.model('TagSearch', {    
    'q': fields.String(required = False)
})

tagList_model = api.model('TagList', {
    'tags': fields.List(fields.String)
})

category_search_model = api.model('CategorySearch', {
    'group': fields.String()
})

category_model = api.model('Category', {
    'name': fields.String,
    'tags': fields.List(fields.String)
})

tagCategoryList_model = api.model('TagCategoryList', {
    'categories': fields.List(fields.Nested(category_model))
})

tag_search_parser = parserForModel(api, tag_search_model, 'args')
category_search_parser = parserForModel(api, category_search_model, 'args')

@api.route("")
class Tags(Resource):

    @api.require_permissions(PermissionStr.RECIPE_READ)
    @api.expect(tag_search_parser)
    @api.marshal_with(tagList_model)
    def get(self):
        '''
        Return a list of tags which match the search term
        '''

        args = tag_search_parser.parse_args()        
        return { 'tags': db_tags_get(args.q) }

@api.route("/categories")
class TagCategories(Resource):
    #@api.require_permissions(PermissionStr.RECIPE_READ)    
    @api.expect(category_search_parser)
    @api.marshal_with(tagCategoryList_model)
    def get(self):
        '''
        Returns the list of existing tag categories
        '''        
        args = category_search_parser.parse_args()        

        categories = db_get_tag_categories(args.group)
        rlist = []
        for c in categories:
            rlist.append({'name': c, 'tags': categories[c]})
        return {'categories': rlist}