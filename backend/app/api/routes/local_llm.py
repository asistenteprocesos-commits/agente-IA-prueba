from fastapi import APIRouter

from app.schemas.local_llm import LocalLLMProfileResponse
from app.services.local_llm_service import LocalLLMService

router = APIRouter()


@router.get("/profile", response_model=LocalLLMProfileResponse)
def get_local_llm_profile() -> LocalLLMProfileResponse:
    return LocalLLMService().get_profile()
