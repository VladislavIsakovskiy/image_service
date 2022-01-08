from httpx import AsyncClient

import pytest

from image_service.app import image_app


@pytest.fixture(scope="module")
async def test_async_client():
    async with AsyncClient(app=image_app, base_url="http://testserver") as client:
        yield client
