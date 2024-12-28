"""Test run file"""
from run import app


async def test_health() -> None:
    """Test health method"""
    test_client = app.test_client()
    response = await test_client.get("/health")
    json_response = await response.get_json()
    assert json_response["status"] == "Online"
