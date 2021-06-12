from typing import Tuple

import responder
import uvicorn
from ratelimit import RateLimitMiddleware, Rule
from ratelimit.auths import EmptyInformation
from ratelimit.backends.redis import RedisBackend
from ratelimit.types import Scope

api = responder.API()


async def unique_header_id(scope: Scope) -> Tuple[str, str]:
    """ Get a unique ID from the header to identify the user. """
    headers = scope["headers"]
    user = None
    for header in headers:
        if header[0].decode() == "unique-user-id":
            user = header[1].decode()

    try:
        return user, "default"
    except KeyError:
        raise EmptyInformation(scope)


api.add_middleware(
    RateLimitMiddleware,
    authenticate=unique_header_id,
    backend=RedisBackend(host="responder_limit_rate_redis"),
    config={
        r"^/rate_limit": [Rule(minute=1, group="default")],
    },
)


@api.route("/no_limit")
def no_limit(req, resp):
    resp.text = "no_limit"


@api.route("/rate_limit")
def rate_limit(req, resp):
    resp.text = "up to one call per minute."


if __name__ == '__main__':
    uvicorn.run("run:api",
                host="0.0.0.0",
                port=8000,
                reload=True,
                log_config='logging.conf',
                log_level='debug',
                access_log=False)
