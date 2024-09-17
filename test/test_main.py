import pytest
from httpx import ASGITransport, AsyncClient
from main import app

@pytest.mark.asyncio
async def test_upload_image():
    image_file_path = "test/test.png"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        with open(image_file_path, "rb") as file:
            response = await client.post("/upload-image/", files={"file": file}, params={"width": 100, "height": 100})
    assert response.status_code == 200
    assert "image_id" in response.json()
    assert "public_url" in response.json()

@pytest.mark.asyncio
async def test_get_image():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        response = await client.get("/get-image/1")
    assert response.status_code == 200
    assert "image_id" in response.json()

@pytest.mark.asyncio
async def test_most_frequent_transformation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        response = await client.get("/most-frequent-transformation")
    assert response.status_code == 200
    assert "transformation_type" in response.json()

@pytest.mark.asyncio
async def test_latest_transformations():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        response = await client.get("/latest-transformations")
    assert response.status_code == 200
    assert "latest_transformations" in response.json()

@pytest.mark.asyncio
async def test_ranking_images():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        response = await client.get("/ranking-images")
    assert response.status_code == 200
    assert "rankings" in response.json()