"""Main configuration file for quart"""

import os
from quart import Quart, ResponseReturnValue  # type: ignore
from quart_auth import QuartAuth  # type: ignore
from quart_rate_limiter import RateLimiter, RateLimitExceeded
from quart_schema import RequestSchemaValidationError
from quart_uploads import configure_uploads, UploadSet


from lib.api_error import APIError

app = Quart(__name__)
app.config.from_prefixed_env(prefix="DH")

auth_manager = QuartAuth(app)
rate_limiter = RateLimiter(app)

upload_set = UploadSet()


@app.errorhandler(APIError)
async def handle_api_error(error: APIError) -> ResponseReturnValue:
    """Error handler for api"""
    return {"code": error.code}, error.status_code


@app.errorhandler(RateLimitExceeded)
async def handle_rate_limit_exceeded_error(
    error: RateLimitExceeded,
) -> ResponseReturnValue:
    """Handle rate limit errors"""
    return {}, error.get_headers(), 429


@app.errorhandler(RequestSchemaValidationError)
async def handle_request_schema_validation_error(
    error: RequestSchemaValidationError,
) -> ResponseReturnValue:
    """Handle request schema validation errors"""
    return {
        "errors": (
            str(error.validation_error)
            if isinstance(error.validation_error, TypeError)
            else error.validtion_error.json()
        )
    }, 400


@app.get("/health")
async def default_route() -> ResponseReturnValue:
    """Initial method to check server status"""
    length = os.getenv("MAX_CONTENT_LENGTH", "notfound")
    print(length)
    return {"status": "Online"}, 200
