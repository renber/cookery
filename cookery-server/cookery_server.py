#
# a flask webserver which provides the REST API for TUC DriveCloud
#

from pyapp import config

import logging
import sys

# setup the root logger first
# log to console and file
logging.basicConfig(level=logging.DEBUG if config.DEBUG else logging.INFO,
handlers=[
    logging.FileHandler("server.log"),
    logging.StreamHandler()
])

logger = logging.getLogger(__name__)

from pyapp.auth import require_permissions
from flask_restx import Resource, Api, Namespace

# patch the Namespace app to contain a permission decorator
# which both configures the auth object to require permissions
# and documents them for Swagger
setattr(Namespace, 'require_permissions', require_permissions)

from flask import Flask, send_file, request
import bcrypt

from pyapp.dao.base import db_init
from pyapp.api import blueprint as rest_api

app = Flask(__name__)
app.register_blueprint(rest_api)

# instantiate the app
if config.DEBUG:
    from flask_cors import CORS
    logger.info("Enabling CORS")
    # enable cross-origin resource sharing only for development
    CORS(app, expose_headers='Authorization')

logger.info("Setting up database connection")
db_init()
# logger.info("Cleaning file cache")
# diskCache.clean()

@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """
    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True

@app.after_request
def add_header(r):
    if r.headers["content-type"].startswith("image/"):
        # allow caching of images
        #r.headers["expires"] = "1y"
        pass
    else:
        # disable caching of API calls
        r.headers["Cache-Control"] = "no-store"
    return r

if __name__ == '__main__':
    logger.info("Starting server")
    app.run(host=config.STANDALONE_HOST, port=config.STANDALONE_PORT, debug=config.DEBUG)