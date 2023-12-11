from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.questao_model import QuestaoModel
from schemas.questao_schema import QuestaoSchema
from core.deps import get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=QuestaoSchema)
async def post_questao(questao: QuestaoSchema, db: AsyncSession = Depends(get_session)):
	
	nova_questao = QuestaoModel(texto=questao.texto, assunto=questao.assunto)
	db.add(nova_questao)
	await db.commit()
	return nova_questao


# Get questaos
@router.get('/', response_model=List[QuestaoSchema])
async def get_questoes(db: AsyncSession = Depends(get_session)):
	async with db as session:
		query = select(QuestaoModel)
		result = await session.execute(query)
		questoes: List[QuestaoModel] = result.scalars().all()
		return questoes
	

# get questao
@router.get('/{questao_id}', response_model=QuestaoSchema, \
			status_code=status.HTTP_200_OK)
async def get_questao(questao_id: int, db:AsyncSession = Depends(get_session)):
	async with db as session:
		query = select(QuestaoModel).filter(QuestaoModel.id == questao_id)
		result = await session.execute
		questao = result.scalar_one_or_none()

		if questao:
			return questao
		else:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
					   detail=f'Questao {questao_id} não encontrada!')
		


# PUT questao
@router.put('/{questao_id}', response_model=QuestaoSchema, \
			status_code=status.HTTP_200_OK)
async def put_questao(questao_id: int, \
					  questao: QuestaoSchema, \
					  db: AsyncSession = Depends(get_session)):
	async with db as session:
		query = select(QuestaoModel).filter(QuestaoModel.id == questao_id)
		result = await session.execute(query)
		questao_up = result.scalar_one_or_none()

		if questao_up:
			questao_up.texto = questao.texto
			questao_up.assunto = questao.assunto

			await session.commit()
			return questao_up
		else:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, \
								detail=f'Questao {questao_id} não encontrada!')
		
# DELETE questao
@router.delete('/{questao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_questao(questao_id: int, \
						 db: AsyncSession = Depends(get_session)):
	async with db as session:
		query = select(QuestaoModel).filter(QuestaoModel.id == questao_id)
		result = await session.execute(query)
		questao_del = result.scalar_one_or_none()

		if questao_del:
			await session.delete(questao_del)
			await session.commit()
			return Response(status_code=status.HTTP_204_NO_CONTENT)
		else:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, \
								detail=f'Questao {questao_id} não encontrada!')

	