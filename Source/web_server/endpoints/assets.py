from web_server._logic import web_server_handler, server_path
import assets.returns as returns
import util.const


@server_path("/asset")
@server_path("/asset/")
@server_path("/v1/asset")
@server_path("/v1/asset/")
@server_path("/.127.0.0.1/asset/")
def _(self: web_server_handler) -> bool:
    assets = self.server.game_config.asset_cache

    # Paramater can either be `id` or `assetversionid`.
    asset_id = assets.resolve_asset_query(self.query)

    if (
        asset_id == util.const.PLACE_ID_CONST
        and self.domain != 'localhost'
    ):
        self.send_error(
            403,
            "Server hosters don't tend to like exposing their place files.  " +
            "Ask them if they'd be willing to lend this one to you.",
        )
        return True

    asset = assets.get_asset(asset_id)
    if isinstance(asset, returns.ret_data):
        self.send_data(asset.data)
        return True
    elif isinstance(asset, returns.ret_none):
        self.send_error(404)
        return True
    elif isinstance(asset, returns.ret_redirect):
        self.send_response(301)
        self.send_header("Location", asset.url)
        self.end_headers()
        return True
    return False


@server_path('/ownership/hasasset', commands={'GET'})
def _(self: web_server_handler) -> bool:
    '''
    Typically used to check if players own specific catalogue items.
    There are no current plans to implement catalogue APIs in RFD.
    Collective ownership it is...
    '''
    self.send_json('true')
    return True
