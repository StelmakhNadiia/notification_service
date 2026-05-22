import pytest
from httpx import AsyncClient, ASGITransport
from app import create_app

@pytest.mark.asyncio
async def test_health_check_success(mocker):
    mock_session = mocker.MagicMock()
    mock_session.execute = mocker.AsyncMock()

    mock_context = mocker.MagicMock()
    mock_context.__aenter__ = mocker.AsyncMock(return_value=mock_session)
    mock_context.__aexit__ = mocker.AsyncMock()

    mocker.patch("app.controllers.http_routes.AsyncSessionLocal", return_value=mock_context)
    
    app = create_app()
    
   
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
        
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["dependencies"]["database"] == "connected"


@pytest.mark.asyncio
async def test_health_check_database_down(mocker):

    mock_context = mocker.MagicMock()
    mock_context.__aenter__ = mocker.AsyncMock(side_effect=ConnectionError("Database connection refused"))
    mock_context.__aexit__ = mocker.AsyncMock()

    mocker.patch("app.controllers.http_routes.AsyncSessionLocal", return_value=mock_context)
    
    app = create_app()
    
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
        
    assert response.status_code == 503
    assert response.json()["status"] == "unhealthy"
    assert response.json()["dependencies"]["database"] == "disconnected"