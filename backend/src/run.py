"""Main configuration file for quart"""
from quart import Quart, ResponseReturnValue

app = Quart(__name__)


@app.get("/health")
async def default_route() -> ResponseReturnValue:
    """Initial method to check server status"""
    return {"status": "Online"}
