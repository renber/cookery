import logging

from flask import Blueprint, url_for
from flask_restx import Api
2145
from pyapp.api.user import api as user_api
from pyapp.api.recipes import api as recipes_api
from pyapp.api.tags import api as tags_api
from pyapp.api.ingredients import api as ingredients_api
from pyapp.api.management import api as management_api
from pyapp import config

logger = logging.getLogger(__name__)

@property
def specs_url(self):
    return config.BASE_URL + '/api/v1/swagger.json'

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

if not config.DEBUG:
    print("Adjusting specs_url to HTTPS")
    # fix swagger url when serving over https in production
    Api.specs_url = specs_url

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
cookery_api = Api(blueprint, title="Cookery ReST API",
    security='Bearer Auth', authorizations=authorizations,    
    doc='/doc', version='1.0')

# add API endpoints
cookery_api.add_namespace(user_api, path='/user')
cookery_api.add_namespace(recipes_api, path='/recipes')
cookery_api.add_namespace(tags_api, path='/tags')
cookery_api.add_namespace(ingredients_api, path='/ingredients')
cookery_api.add_namespace(management_api, path='/management')