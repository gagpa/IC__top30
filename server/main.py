from typing import Dict

from api import make_app
from base_schemas import OkResponse

app = make_app()


@app.get("/healthz", tags=["health check"], response_model=OkResponse)
async def root() -> Dict[str, bool]:
    """Health check endpoint"""
    return {"ok": True}
