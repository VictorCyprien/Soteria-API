import logging
import logging.config

from environs import Env

class Config:

    def __init__(self):
        env = Env()

        self.SERVICE_NAME = 'soteria-api'
        self.LOGGER_LEVEL = env.str("LOGGER_LEVEL", "INFO")

        #BungieAPI
        self.BUNGIE_API_KEY = env.str("BUNGIE_API_KEY", "")
        self.BUNGIE_API_CLIENT_ID = env.int("BUNGIE_API_CLIENT_ID", None)
        self.BUNGIE_API_CLIENT_SECRET = env.str("BUNGIE_API_CLIENT_SECRET", "")

    @property
    def logger_config(self):
        return {
            'version': 1,
            'formatters': {
                'color_formatter': {
                    '()': 'colorlog.ColoredFormatter',
                    'format': "%(log_color)s%(asctime)s | %(levelname)-8s | %(message)s"
                }
            },
            'handlers': {
                'console': {
                    'class': 'colorlog.StreamHandler',
                    'level': self.LOGGER_LEVEL,
                    'formatter': 'color_formatter'
                },
            },
            'loggers': {
                'console': {
                    'level': self.LOGGER_LEVEL,
                    'propagate': False,
                    'handlers': ['console']
                }
            }
        }

    def configure_logging(self):
        logging.config.dictConfig(self.logger_config)

    @property
    def json(self):
        return {key: self.__getattribute__(key) for key in self.__dir__() if not key.startswith('_') and key.isupper()}

    def validate(self):
        if not self.BUNGIE_API_KEY:
            raise ValueError("The BungieAPI Key is not filled !")
        
        if not self.BUNGIE_API_CLIENT_ID:
            raise ValueError("The BungieAPI Client ID is not filled !")
        
        if not self.BUNGIE_API_CLIENT_SECRET:
            raise ValueError("The BungieAPI Client Secret is not filled !")


config = Config()
