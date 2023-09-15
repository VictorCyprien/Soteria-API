from aiohttp import web
from aiohttp.web_exceptions import HTTPUnauthorized


# Routes with no auth needed
routes_list = ["", "login", "redirect"]


@web.middleware
async def auth_middleware(request, handler):
    # We check if we need to have auth informations in header to processed
    # We take the route name only
    current_route = str(request.url).split("/")[3]
    
    # Remove query params because it's not matching (even with startswith...)
    if "?" in current_route:
        current_route = current_route.split("?")[0]

    for one_route in routes_list:
        if one_route.startswith(current_route):
            return await handler(request)
    # Check access token
    access_token = await check_access_token(request)
    if not access_token:
        raise HTTPUnauthorized(text="Not Authenticated")

    # Check user_id
    user_id = await check_user_id(request)
    if not user_id:
        raise HTTPUnauthorized(text="Not Authenticated")

    # Call method view
    return await handler(request)


async def check_access_token(request):
    # Get access token in headers
    access_token = request.headers.get('X-Access-Token', None)
    if access_token is None:
        return None
    return str(access_token)


async def check_user_id(request):
    # Get user_id in headers
    user_id = request.headers.get('X-Bungie-Userid', None)
    if user_id is None:
        return None
    return int(user_id)
