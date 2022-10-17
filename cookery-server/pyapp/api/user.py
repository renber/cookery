from flask import request
from flask_restx import Namespace, Resource, fields
import bcrypt
from pyapp.auth import auth, parseAuthHeader
from pyapp.permissions import PermissionStr
from pyapp.session import sessionMgr, TokenStatus, getCurrentSession
from pyapp.dao.base import orm
from pyapp.dao.entities import User
from pyapp.dao.user import db_is_usr_active, db_usr_get, db_get_pwd, db_usr_get_permissions
from pyapp.api.utils import parserForModel

import logging
logger = logging.getLogger(__name__)

api = Namespace('user', description='User account management & authorization')

credential_data = api.model("User credentials", {
    "username": fields.String(required=True),
    "password": fields.String(required=True),
})
credential_parser = parserForModel(api, credential_data, "json")

change_password_data = api.model("Password", {
    "old_password": fields.String(required=True),
    "new_password": fields.String(required=True),
})
change_password_parser = parserForModel(api, change_password_data, "json")


@api.route("/login")
class Login(Resource):

    @api.expect(credential_data)
    @orm.db_session
    @api.response(200, 'Credentials were correct', api.model('Authorization', {
    'user': fields.String, 'displayName': fields.String, 'token': fields.String}))
    @api.response(401, 'Wrong username / password combination or user account disabled')
    @api.doc(security=None)
    def post(self):
        '''
        Retrieve an authorization token for the given user
        '''
        args = credential_parser.parse_args()

        print("Received login request by user " + args.username)

        # check if user account exists and is active
        if not db_is_usr_active(args.username):
            print("User account does not exist / is disabled")
            return '', 401

        # check username and password
        hashed_password = db_get_pwd(args.username)

        if not bcrypt.checkpw(args.password.encode('utf-8'), hashed_password):
            print('Wrong password')
            return '', 401

        userinfo = db_usr_get(args.username)

        token = sessionMgr.newSession(userinfo.usr_email, userinfo.usr_uid)

        return {
            "user": userinfo.usr_email,
            "displayName": userinfo.usr_name,
            "token": token
        }

@api.route("/logout")
class Logout(Resource):

    @auth.login_required(role=[PermissionStr.SESSION_TOKEN])
    @api.response(200, 'User has been logged out')
    def get(self):
        '''
        Clears the session identified by the token in the Authorization header
        '''
        auth = request.headers.get('Authorization')
        valid, token = parseAuthHeader(auth)

        if valid:
            print("Received logout request with token " + token)

            if sessionMgr.getTokenStatus(token) == TokenStatus.SESSION_TOKEN_VALID:
                sessionMgr.clearSession(token)

            return 'user logged out', 200

        return '', 401

@api.route("/my/password")
class Password(Resource):

    @api.expect(change_password_data)
    @orm.db_session
    @auth.login_required(role = [PermissionStr.SESSION_TOKEN])
    def post(self):
        '''
        Update the user's password
        '''
        session = getCurrentSession()
        if session == None:
            api.abort(400)
        
        args = change_password_parser.parse_args()        

        # check password
        user = User[session.userid]

        hashed_password = db_get_pwd(user.usr_name)

        if not bcrypt.checkpw(args.old_password.encode('utf-8'), hashed_password):            
            return 'Wrong password', 400

        if len(args.new_password) < 8:
            return 'New password does not match password policy', 400            

        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(args.new_password.encode('utf-8'), salt)

        user.usr_password = hash

        logger.info("Password was changed successfully")    
        return 200  

@api.route("/my/permissions")
class Permissions(Resource):

    @auth.login_required(role = [PermissionStr.SESSION_TOKEN])
    def get(self):
        '''
        Return the permission set of the currently logged in user
        '''
        session = getCurrentSession()
        if session == None:
            api.abort(400)

        return list(map(lambda x: x.value, db_usr_get_permissions(session.userid)))

@api.route("/register")
class Register(Resource):
    
    def post(self):        
        '''
        Register for a new user account.
        After registration the account needs to be activated by an administrator        
        '''
        return 400