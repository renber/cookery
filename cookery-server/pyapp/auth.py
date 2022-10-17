import types
from flask import abort
from flask_httpauth import HTTPTokenAuth
from pyapp.session import sessionMgr, TokenStatus
from pyapp.permissions import PermissionStr
from pyapp.dao.user import db_usr_get_permissions

# Cookery uses token authentication:
# Session Tokens - obtained by using the login API endpoint (username and password), only valid short amount of time (i.e. web session)

auth = HTTPTokenAuth(scheme='Bearer')

def require_permissions(self, *perms):
    '''
    Decorator which both applies login_required with the given role(s)
    and documents required permissions.
    (Will be attached to flask_restx's Namespace class at runtime)
    '''
    decorator1 = auth.login_required(role=perms)

    if len(perms) == 0:
        # no need to document permissions
        return decorator1

    plist = list(map(lambda p: p.value, perms))
    plist.sort()
    decorator2 = self.doc(description = f"<b>Required Permissions:</b> {', '.join(plist)}")

    # create a function decorator that applies the two
    # decorators we just created
    def real_decorator(func):
        return decorator1(decorator2(func))

    return real_decorator

def parseAuthHeader(token):
    '''
    Extracts the token from a HTTP Authorization header value
    of the form [scheme] [token]

    1st return value: bool - syntactical validity of token/scheme
    2nd return value: token, if valid is true
    '''

    if token is None or len(token) == 0:
        return False, ''

    # atm we only support the Bearer scheme
    parts = token.split(' ', 1)
    if len(parts) != 2 or parts[0] != 'Bearer':
        print("Encountered unsupported auth scheme or token: " + token)
        return False, ''

    return True, parts[1]

@auth.verify_token
def verify_token(token):
    if not token or len(token) == 0:
        return False

    print("Received token " + token)

    # check if token is a session token
    token_state, userid = sessionMgr.getTokenStatus(token)
    if token_state == TokenStatus.SESSION_TOKEN_VALID:
        print("Authorized with VALID session token: " + token)
        return {'token': token, 'userid': userid, 'type': 'session'}
        
    # token was neither a valid session nor api token
    print("Authorized with INVALID or expired token: " + token)
    return None

@auth.get_user_roles
def get_user_roles(token_info):    
    if token_info['type'] == 'session':        
        print(f'getting roles for session token for user id {token_info["userid"]}')
        permissions = [PermissionStr.SESSION_TOKEN]
        permissions.extend(db_usr_get_permissions(token_info["userid"]))                
        return permissions    

@auth.error_handler
def auth_error(status):
    # define a global authentication error handler
    # to avoid that flask-restplus marshals the error response
    # use flask to abort the current request
    abort(status)