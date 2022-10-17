from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from pyapp.permissions import PermissionStr
from pyapp.auth import auth
from pyapp.api.utils import parserForModel
from pyapp.dao.user import db_usr_get_permissions, db_users_get
from pyapp.permissions import PermissionStr
import sys

api = Namespace('management', description='System management functions (all require administrative privileges)',
      # all methods need authorization + admin privileges
      decorators=[auth.login_required(role = [PermissionStr.ADMIN, PermissionStr.SESSION_TOKEN])])

new_user_model = api.model('Create User', {    
    'email': fields.String(attribute='usr_email'),
    'name': fields.String(attribute='usr_name'),
    'active': fields.Boolean(attribute='usr_active')   
})

user_model = api.model('User', {
    'id': fields.String(attribute='usr_id'),
    'email': fields.String(attribute='usr_email'),
    'name': fields.String(attribute='usr_name'),
    'active': fields.Boolean(attribute='usr_active')   
})

@api.route("/users")
class Users(Resource):
        
    @api.marshal_list_with(user_model)
    def get(self):        
        '''
        Return the list of registered users
        '''
        return list(db_users_get())

@api.route("/users/create")
class CreateUser(Resource):
    
    @api.expect(new_user_model)
    def post(self):        
        '''
        Creates a new user account
        '''
        return 200

@api.route("/users/<userid>/permissions")
class UserPermissions(Resource):

    def get(self, userid):
        '''
        Return a list of all permissions the user has
        '''        
        return list(map(lambda x: x.value, db_usr_get_permissions(userid)))