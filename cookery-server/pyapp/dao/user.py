from pyapp.dao.base import orm
from pyapp.permissions import PermissionStr
from pyapp.dao.entities import User, Role, Permission

@orm.db_session
def db_is_usr_active(uname):
    # todo: case insensitive comparison
    return orm.select(u.usr_active for u in User if u.usr_name == uname and u.usr_active)[:]

@orm.db_session
def db_get_pwd(uname):
    # todo: case insensitive comparison
    return orm.select(u.usr_password for u in User if u.usr_name == uname).first()

@orm.db_session
def db_usr_set_pwd(uname, newpwd_hash):
    # todo: case insensitive comparison
    user = User.get(usr_name=uname)
    user.usr_password = newpwd_hash

@orm.db_session
def db_users_get():
    return User.select()[:]

@orm.db_session
def db_usr_get(uname):
    '''
    Retrieve information about the user with the given username
    '''
    return User.get(usr_name=uname)

@orm.db_session
def db_usr_get_permissions(userid):
    # is user admin? -> automatically has all permissions    
    if User[userid].usr_isadmin:
        lst = [p for p in PermissionStr if not p.value.startswith('$')]
        lst.append(PermissionStr.ADMIN)
        return lst
    else:
        # return the granted permissions for the role the user has      
        # avoid virtual permissions coming in through the database  
        pvalues = orm.select(p.perm_granted for p in Permission for u in User 
                  if u.usr_uid == userid and p.perm_roleid == u.usr_roleid and not p.perm_granted.startswith('$'))

        # return the PermissionStr instances instead of strings
        return list(map(lambda p: PermissionStr(p), pvalues))