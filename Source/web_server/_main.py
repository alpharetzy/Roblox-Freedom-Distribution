import web_server.logic

# Make sure all API endpoints are working without taking anything therefrom.
from .endpoints._main import _


def make_server(port_num=80, *args, **kwargs) -> web_server.logic.web_server:
    return web_server.logic.web_server(('', port_num), *args, **kwargs)
