"""Main configuration file for quart"""

import os
import json
import asyncio
from os.path import join, dirname, abspath
from dotenv import load_dotenv
from quart import Quart, ResponseReturnValue  # type: ignore
from quart_auth import QuartAuth  # type: ignore
from quart_rate_limiter import RateLimiter, RateLimitExceeded
from quart_schema import RequestSchemaValidationError
from blueprints.file_services import blueprint as file_blueprint
from blueprints.query_services import blueprint as query_blueprint
from quart_cors import cors


from lib.api_error import APIError

env_name = os.getenv('QUART_ENV')

dotenv_path = abspath(
    join(dirname(__file__), '..', f'{env_name}.env')
)

load_dotenv(dotenv_path=dotenv_path)


settings = {
    "allow_origin": "*",
    "allow_methods": "*"
}

app = Quart(__name__)
app = cors(app, allow_origin="*")
app.config.from_prefixed_env(prefix="DH")

auth_manager = QuartAuth(app)
rate_limiter = RateLimiter(app)

app.register_blueprint(file_blueprint)
app.register_blueprint(query_blueprint)


@app.errorhandler(APIError)
async def handle_api_error(error: APIError) -> ResponseReturnValue:
    """Error handler for api"""
    return {"code": error.code}, error.status_code


@app.errorhandler(RateLimitExceeded)
async def handle_rate_limit_exceeded_error(
    error: RateLimitExceeded,
) -> ResponseReturnValue:
    """Handle rate limit errors"""
    return {}, 429, error.get_headers()


@app.errorhandler(RequestSchemaValidationError)
async def handle_request_schema_validation_error(
    error: RequestSchemaValidationError,
) -> ResponseReturnValue:
    """Handle request schema validation errors"""
    return {
        "errors": (
            str(error.validation_error)
            if isinstance(error.validation_error, TypeError)
            else json.dumps(error.validation_error.__dict__)
        )
    }, 400


@app.get("/health")
async def default_route() -> ResponseReturnValue:
    """Initial method to check server status"""
    print(os.getenv("DH_QUART_AUTH_COOKIE_SAMESITE"))
    length = os.getenv("MAX_CONTENT_LENGTH", "notfound")
    print(length)
    return {"status": "Online"}, 200


if __name__ == "__main__":
    asyncio.run(app.run_task())
