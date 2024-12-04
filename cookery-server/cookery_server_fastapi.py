from pyapp import config

import logging

# setup the root logger first
# log to console and file
logging.basicConfig(level=logging.DEBUG if config.DEBUG else logging.INFO,
handlers=[
    logging.FileHandler("server_fastapi.log"),
    logging.StreamHandler()
])

logger = logging.getLogger(__name__)

from pyapp.newapi import app
from pyapp.dao.base import db_init


logger.info("Setting up database connection")
db_init()

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting server")
    uvicorn.run(app, host=config.STANDALONE_HOST, port=config.STANDALONE_PORT)
