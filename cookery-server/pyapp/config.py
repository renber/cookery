import configparser


cfg = configparser.ConfigParser()
try:
    print(f'Reading config from "cookery_server_config.ini"')
    cfg.read('cookery_server_config.ini')

    BASE_URL = cfg.get('general', 'base_url', fallback='')
    DEBUG = cfg.getboolean('general', 'debug', fallback=False)

    STANDALONE_HOST = cfg.get('standalone', 'host', fallback='127.0.0.1')
    STANDALONE_PORT = cfg.get('standalone', 'port', fallback=3333)

    DATABASE_HOST = cfg.get('database', 'host')
    DATABASE_USER = cfg.get('database', 'user')
    DATABASE_PASSWORD = cfg.get('database', 'password')
    DATABASE_DBNAME = cfg.get('database', 'database')
    DATABASE_TABLE_PREFIX = cfg.get('database', 'table_prefix', fallback='')   

    STORE_FOLDER = cfg.get('store', 'folder', fallback='./store')
    IMAGE_STORE_FOLDER = STORE_FOLDER + '/images'


except Exception as e:
        print("Invalid or missing configuration file: ", str(e))
        exit(-1)