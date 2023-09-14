"""Main app"""
from api.main import app, ctx
from aiohttp import web

if __name__ == '__main__':
    web.run_app(app, ssl_context=ctx, port=5000)
