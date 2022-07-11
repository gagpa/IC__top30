from fastapi import APIRouter, Depends

from api_v1.base.client_requests import Client
from api_v1.base.dependencies import get__client
import domain
router = APIRouter(tags=['События'], prefix='/event')


# @router.get(
#     '/'
# )
# async def _filter(
#         client: Client = Depends(get__client),
#         filter_events__case: domain.event
# ):
#
