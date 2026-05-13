from fastapi import APIRouter

from app.api.routes import (
    bpmn,
    health,
    knowledge,
    local_llm,
    orchestration,
    process_analysis,
    process_cases,
    process_deliverables,
    process_discovery,
    process_redesign,
    process_repositories,
    process_simulation,
)

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(local_llm.router, prefix="/local-llm", tags=["local llm"])
api_router.include_router(
    orchestration.router,
    prefix="/process-cases",
    tags=["orchestration"],
)
api_router.include_router(
    bpmn.router,
    prefix="/process-cases",
    tags=["bpmn"],
)
api_router.include_router(
    process_analysis.router,
    prefix="/process-cases",
    tags=["process analysis"],
)
api_router.include_router(
    process_redesign.router,
    prefix="/process-cases",
    tags=["process redesign"],
)
api_router.include_router(
    process_simulation.router,
    prefix="/process-cases",
    tags=["process simulation"],
)
api_router.include_router(
    process_deliverables.router,
    prefix="/process-cases",
    tags=["process deliverables"],
)
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
