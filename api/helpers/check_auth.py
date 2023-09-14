from aiohttp import web
from aiohttp.web_exceptions import HTTPUnauthorized


# Routes with no auth needed
routes_list = ["/", "/login", "/redirect"]


@web.middleware
async def auth_middleware(request, handler):
    # We check if we need to have auth informations in header to processed
    for one_route in routes_list:
        if one_route in str(request.url):
            return await handler(request)
        
    # Check access token
    access_token = await check_access_token
    if not access_token:
        raise HTTPUnauthorized(text="Not Authenticated")

    # Check user_id
    user_id = await check_user_id(request)
    if not user_id:
        raise HTTPUnauthorized(text="Not Authenticated")

    # Call method view
    return await handler(request)


async def check_access_token(request):
    # Get user_id in headers
    access_token = request.headers.get('X-Access-Token')
    if not access_token:
        return None
    return str(access_token)


async def check_user_id(request):
    # Get user_id in headers
    user_id = request.headers.get('X-Bungie-Userid')
    if not user_id:
        return None
    return int(user_id)
