from typing import Optional
from datetime import datetime

from pydantic import BaseModel as SCBaseModel


class QuestaoSchema(SCBaseModel):
	id: Optional[int]
	data_criacao: Optional[datetime] = datetime.now
	texto: str
	assunto: Optional[str]

	class Config:
		orm_mode = True