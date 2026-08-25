from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Response, Request


from app.config import settings
from app.codes import generate_code, validate_url
from app.store import get_store
from app.store.base import CodeCollision, Link


app = FastAPI()

store = get_store(settings)





@app.post("/api/shorten", status_code=201)
async def shorten(request: Request):
    data = await request.json()

    if "url" not in data:
        raise HTTPException(status_code=400, detail="url is required")

    try:
        target_url = validate_url(data["url"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    for _ in range(5):
        link = Link(
            code=generate_code(),
            target_url=target_url,
            created_at=datetime.now(timezone.utc)
        )

        try:
            await store.put(link)
            return {
                "code": link.code,
                "short_url": f"{settings.base_url}/{link.code}",
                "target_url": link.target_url,
                "created_at": link.created_at.isoformat()
            }
        except CodeCollision:
            continue

    raise HTTPException(
        status_code=500,
        detail="could not allocate a unique code"
    )
@app.get("/healthz")
async def healthz(response: Response):
    if await store.health():
        return {"status": "ok"}

    response.status_code = 503
    return {
        "status": "degraded",
        "detail": "store unreachable"
    }
@app.get("/{code}")
async def redirect(code: str):
    link = await store.get(code)

    if link is None:
        raise HTTPException(status_code=404, detail="code not found")

    await store.increment_clicks(code)

    return Response(
        status_code=302,
        headers={"Location": link.target_url}
    )



@app.get("/api/stats/{code}")
async def stats(code: str):
    link = await store.get(code)

    if link is None:
        raise HTTPException(status_code=404, detail="code not found")

    return {
        "code": link.code,
        "target_url": link.target_url,
        "clicks": link.clicks,
        "created_at": link.created_at.isoformat()
    }

