
# Data Access Object
# Abstracts the database connection away
# Uses PonyORM for database access https://ponyorm.org

import re
from pony import orm
from datetime import datetime, timedelta
import uuid
from pony.orm.dbapiprovider import StrConverter
from enum import Enum
from pyapp import config

REQUIRED_DATABASE_VERSION = '1'

def tablename(baseName):
    return config.DATABASE_TABLE_PREFIX + baseName

def _contract(tuple, *args):
    '''
    Contracts the given tuple to a single object
    where all tuple elements are added as attributes to the first
    tuple using the attribute names given
    '''
    t = tuple[0]
    for i in range(0, len(args[0])):
        setattr(t, args[0][i], tuple[1 + i])

    return t

def _contract_list(tuple_list, *args):
    '''
    Converts the list of tuples to a list of
    contracted tuples
    (can be used to convert result of Pony join selects)
    '''
    return list(map(lambda x: _contract(x, args), tuple_list))

def gen_row_id():
    '''
    Generates a new, globally unique id for a table row
    '''
    return str(uuid.uuid4())

db = orm.Database()

class CookerySystemDatabase(db.Entity):
    '''
    Table which contains system info
    '''
    _table_ = [tablename('SYSTEM')]

    sys_property = orm.PrimaryKey(str)
    sys_val = orm.Optional(str)

@orm.db_session()
def db_check_version():
    try:
        dbv = CookerySystemDatabase['DATABASE_VERSION']
        if dbv.sys_val != REQUIRED_DATABASE_VERSION:
            raise Exception(f'Wrong database version: {dbv.sys_val} (server requires: {REQUIRED_DATABASE_VERSION})')
    except Exception as e:
        raise Exception(f'Error while checking database version. Ensure that database is configured correctly: {e}')

def db_init():    
    db.bind(provider='mysql', host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASSWORD, db=config.DATABASE_DBNAME)
    db.provider.converter_classes.append((Enum, EnumConverter))
    db.generate_mapping(create_tables=False,check_tables=False)
    orm.set_sql_debug(config.DEBUG)

    db_check_version()

class EnumConverter(StrConverter):
    '''
    Support for storing/reading Enums with Pony
    '''

    def validate(self, val, obj=None):
        if not isinstance(val, Enum):
            raise ValueError('Must be an Enum.  Got {}'.format(type(val)))
        return val

    def py2sql(self, val):
        return val.name

    def sql2py(self, value):
        # Any enum type can be used, so py_type ensures the correct one is used to create the enum instance
        return self.py_type[value]    