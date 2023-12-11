from fastapi import APIRouter

from api.v1.endpoints import questao



api_router = APIRouter()
api_router.include_router(questao.router, prefix='/questoes', tags=['cursos'])