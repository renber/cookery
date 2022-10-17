from enum import Enum 

# This file defines all available permissions
# which can be assigned to roles (and thus users)
# To mark that an api request requires a specific permission
# use @auth.require_permissions(role=[...]), e.g. @auth.require_permissions(role=[PermissionRole.UPLOAD])

# permissions prefixed with a dollar sign ($) are virtual
# and automatically added by the authentication system
# they cannot be granted manually

class PermissionStr(Enum):
    # the function needs to be called with a session token
    SESSION_TOKEN = '$session_token'

    # the function needs to be called by an administrator
    # (allows management functions to be used)
    ADMIN = '$admin_privileges'
    
    # function permissions
    RECIPE_READ = 'recipe:read'
    RECIPE_WRITE = 'recipe:write'

    INGREDIENT_READ = 'ingredient:read'
    INGREDIENT_WRITE = 'ingredient:write'