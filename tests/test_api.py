# tests/test_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_shorten_returns_code(client: AsyncClient):
    r = await client.post("/api/shorten", json={"url": "https://example.com/x"})
    assert r.status_code == 201
    assert len(r.json()["code"]) == 7

@pytest.mark.anyio
async def test_redirect_sends_302_with_location(client: AsyncClient):
    code = (await client.post("/api/shorten",
            json={"url": "https://example.com/x"})).json()["code"]
    r = await client.get(f"/{code}", follow_redirects=False)
    assert r.status_code == 302
    assert r.headers["location"] == "https://example.com/x"

@pytest.mark.anyio
async def test_unknown_code_is_404(client: AsyncClient):
    assert (await client.get("/nope123", follow_redirects=False)).status_code == 404

@pytest.mark.anyio
async def test_rejects_non_http_scheme(client: AsyncClient):
    r = await client.post("/api/shorten", json={"url": "javascript:alert(1)"})
    assert r.status_code == 400

@pytest.mark.anyio
async def test_rejects_missing_url(client: AsyncClient):
    assert (await client.post("/api/shorten", json={})).status_code == 400

@pytest.mark.anyio
async def test_clicks_are_counted(client: AsyncClient):
    code = (await client.post("/api/shorten",
            json={"url": "https://example.com/y"})).json()["code"]
    for _ in range(3):
        await client.get(f"/{code}", follow_redirects=False)
    assert (await client.get(f"/api/stats/{code}")).json()["clicks"] == 3

@pytest.mark.anyio
async def test_healthz_reports_store_state(client: AsyncClient):
    assert (await client.get("/healthz")).status_code == 200

@pytest.mark.anyio
async def test_codes_are_unique_across_many_calls(client: AsyncClient):
    codes = set()
    for _ in range(200):
        codes.add((await client.post("/api/shorten",
                   json={"url": "https://example.com/z"})).json()["code"])
    assert len(codes) == 200