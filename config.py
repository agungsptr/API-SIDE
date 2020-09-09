import datetime


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "7Bs6vcBuoJQ97XnKNUbO2C4wvdwGPIzj14JQE3k2fdDdt0ihTJcbA" \
                 "PuDtyxmzbL_SIfaStBM3lUyFN0SJxdGwJ4hoZd-UjVsDWmmtU4Yot" \
                 "uSg_hMUz5DRJKtDiRLo0LQghjwQpqveot9w8G5as7JR7ppvVdZfcM" \
                 "wYYAtgDltJa8"
    DB_HOST = "127.0.0.1"
    DB_USERNAME = "root"
    DB_PASSWORD = ""
    DB_PORT = 3306
    DB_NAME = "side"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECK = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)


class Production(Config):
    pass


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True
