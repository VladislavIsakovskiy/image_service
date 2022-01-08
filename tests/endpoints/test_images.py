import json

import pytest


@pytest.mark.asyncio
async def test_read_images(test_async_client):  # noqa
    response = await test_async_client.get("/v1/images/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_image_success(test_async_client):  # noqa
    response = await test_async_client.get("/v1/images/1.jpg/")
    assert response.status_code == 200
    response_info_keys = json.loads(response.content).keys()
    assert {"name", "size", "last_change_time"} == response_info_keys


@pytest.mark.asyncio
async def test_read_non_existed_image_raise_exception(test_async_client):  # noqa
    response = await test_async_client.get("/v1/images/3.jpg/")
    assert response.status_code == 422
    message = json.loads(response.content)["message"]
    assert message == "There is no image 3.jpg at server."


@pytest.mark.asyncio
async def test_upload_image_from_bytes_success(test_async_client):  # noqa
    with open("../files/image_b64_str.txt", "r", encoding="cp1251") as f:
        image_bytes = f.read()
    request_data = {
        "name": "3.jpg",
        "image_str": image_bytes,
    }
    response = await test_async_client.post("/v1/images/upload_image_from_bytes", json=request_data)
    assert response.status_code == 200
    message = json.loads(response.content)["message"]
    assert message == "Image 3.jpg uploaded successfully!"


@pytest.mark.asyncio
async def test_upload_existed_name_image_from_bytes_raise_exception(test_async_client):  # noqa
    with open("../files/image_b64_str.txt", "r", encoding="cp1251") as f:
        image_bytes = f.read()
    request_data = {
        "name": "3.jpg",
        "image_str": image_bytes,
    }
    response = await test_async_client.post("/v1/images/upload_image_from_bytes", json=request_data)
    assert response.status_code == 409
    message = json.loads(response.content)["message"]
    assert message == "Image with 3.jpg name already exists. Please, choose other name."


@pytest.mark.asyncio
async def test_delete_non_existed_image_raise_exception(test_async_client):  # noqa
    response = await test_async_client.get("/v1/images/4.jpg/delete")
    assert response.status_code == 422
    message = json.loads(response.content)["message"]
    assert message == "There is no image 4.jpg at server."


@pytest.mark.asyncio
async def test_delete_image_success(test_async_client):  # noqa
    response = await test_async_client.get("/v1/images/3.jpg/delete")
    assert response.status_code == 200
    message = json.loads(response.content)["message"]
    assert message == "Image 3.jpg deleted successfully!"
