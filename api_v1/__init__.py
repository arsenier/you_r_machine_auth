from fastapi import APIRouter

from .users.views import router as users_router
from .demo_auth.views import router as demo_auth_router

router = APIRouter()
router.include_router(router=users_router, prefix="/oauth/users")
router.include_router(router=demo_auth_router, prefix="/oauth")
