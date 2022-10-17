from flask import request
import uuid
from datetime import datetime, timedelta
from pyapp.dao.base import orm
from pyapp.dao.entities import Session
from pyapp import config
from enum import Enum 

import logging
logger = logging.getLogger(__name__)

class TokenStatus(Enum):
    SESSION_TOKEN_INVALID = 0
    SESSION_TOKEN_VALID = 1
    SESSION_TOKEN_EXPIRED = -1    

def getTokenFromHeader(token):
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
        logger.warning("Encountered unsupported auth scheme or token: " + token)
        return False, ''

    return True, parts[1]

def getCurrentSession():
    '''
    Return the session of the current request scope
    '''
    header = request.headers.get('Authorization')
    valid, token = getTokenFromHeader(header)
    if not valid:
        return None

    return sessionMgr.getSessionInfo(token)

class SessionMgr:
    '''
    Manages sessions of logged in users
    '''
    _defaultSessionLifetime = timedelta(hours=24) if config.DEBUG else timedelta(minutes=30)

    # _sessions = {}

    def newSession(self, user, userid):
        '''
        Creates a new session and returns the
        corresponding token
        '''
        token = str(uuid.uuid4())
        session = Session(ses_uid = token, ses_userid = userid,
            ses_expires = datetime.now() + self._defaultSessionLifetime)
        session._defaultSessionLifetime = self._defaultSessionLifetime

        logger.debug("Created session " + token)
        return token

    def sessionHasExpired(self, sessioninfo):
        return datetime.now() > sessioninfo.expires

    def getTokenStatus(self, token):
        '''
        Checks if a session with the given token is valid
        Returns one of the following TokenStatus values
        SESSION_TOKEN_INVALID        
        SESSION_TOKEN_EXPIRED
        SESSION_TOKEN_VALID
        If the session is valid teh username is returned as second result           
        '''
        # todo: check if the session has expired
        logger.debug("Checking session '" + token + "'")
        if token is None or token == '':
            return TokenStatus.SESSION_TOKEN_INVALID, None

        session = self.getSessionInfo(token)

        if session == None:
            # token does not exist
            return TokenStatus.SESSION_TOKEN_INVALID, None

        if self.sessionHasExpired(session):
            logger.debug("Session has EXPIRED: " + token)
            self.clearSession(token)
            return TokenStatus.SESSION_TOKEN_EXPIRED, None

        session.touch(self._defaultSessionLifetime)

        return TokenStatus.SESSION_TOKEN_VALID, session.userid

    @orm.db_session
    def getSessionInfo(self, token):
        try:
            ses = Session[token]
            return SessionInfo(ses)
        except:
            return None

    @orm.db_session
    def clearSession(self, token):
        '''
        Delete (i.e end) the session identified by the given token
        '''
        try:
            Session[token].delete()
            logger.debug("Deleted session: " + token)
        except Exception as e:
            logger.error(e)
            pass

    @orm.db_session
    def purge(self):
        '''
        Remove data of all expired sessions
        '''
        Session.select(lambda s: s.ses_expires < datetime.now()).delete(bulk = True)

class SessionInfo:
    '''
    Holds session information (not connected to database)
    '''

    def __init__(self, dbsession):
        self.token = dbsession.ses_uid
        self.userid = dbsession.ses_userid
        self.expires = dbsession.ses_expires

    @orm.db_session
    def touch(self, lifespan):
        self.expires = datetime.now() + lifespan
        # update db
        Session[self.token].ses_expires = self.expires

sessionMgr = SessionMgr()