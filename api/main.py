from environs import Env
Env.read_env()

# Not removed -> Used to initialize faust app
from .config import config
from .app import app, logger, ctx

# Check the current conf
config.validate()
