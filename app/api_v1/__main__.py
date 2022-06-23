import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from db.postgres import create_engine, Base
from settings import AsyncPostgresSettings
from .errors import add_handlers
from .router import add_routers

app = fastapi.FastAPI()

add_routers(app)
add_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def create_tables():
    async with create_engine(AsyncPostgresSettings()).begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080, debug=True)
