"""Main configuration file for quart"""

from quart import Quart, ResponseReturnValue  # type: ignore
from quart_auth import AuthManager # type: ignore
from quart_rate_limiter import  RateLimiter, RateLimitExceeded

from backend.src.lib.api_error import APIError

app = Quart(__name__)
app.config.from_prefixed_env(prefix="DH")

auth_manager = AuthManager(app)
rate_limiter = RateLimiter(app)


@app.errorhandler(APIError)
async def handle_api_error(error: APIError) -> ResponseReturnValue:
    """Error handler for api"""
    return {"code": error.code}, error.status_code


@app.errorhandler(RateLimitExceeded)
async def handle_rate_limit_exceeded_error(
    error: RateLimitExceeded
) -> ResponseReturnValue:
    """Handle rate limit errors"""
    return {}, error.get_headers(), 429


@app.get("/health")
async def default_route() -> ResponseReturnValue:
    """Initial method to check server status"""
    return {"status": "Online"}
