from fastapi import APIRouter

from apis.version1 import route_main_methods
from apis.version1 import route_login
from apis.version1 import route_cards, route_store_chains


api_router = APIRouter()
api_router.include_router(route_main_methods.main_methods_router, prefix="", tags=["main_methods"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
api_router.include_router(route_cards.router, prefix="/cards", tags=["cards"])
api_router.include_router(route_store_chains.router, prefix="/store_chains", tags=["store_chains"])
