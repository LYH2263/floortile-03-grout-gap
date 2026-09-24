from fastapi import APIRouter

from app.repositories import settings_repo
from app.schemas.settings import SettingsUpdate

router = APIRouter(tags=["settings"])


@router.get("/settings")
def get_settings():
    return settings_repo.get_all()


@router.put("/settings")
def update_settings(body: SettingsUpdate):
    settings_repo.set_gap_mm(body.gap_mm)
    return settings_repo.get_all()
