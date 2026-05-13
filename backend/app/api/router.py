from fastapi import APIRouter

from app.api.routes import health, knowledge, local_llm, process_cases, process_discovery, process_repositories

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(local_llm.router, prefix="/local-llm", tags=["local llm"])
api_router.include_router(
    process_repositories.router,
    prefix="/process-cases",
    tags=["process repositories"],
)
api_router.include_router(
    process_discovery.router,
    prefix="/process-cases",
    tags=["process discovery"],
)
api_router.include_router(process_cases.router, prefix="/process-cases", tags=["process cases"])
