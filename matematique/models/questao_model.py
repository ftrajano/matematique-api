from core.configs import settings
from datetime import datetime
from sqlalchemy import DateTime, Integer, String

from sqlalchemy import Column

class QuestaoModel(settings.DBBaseModel):
	__tablename__ = "questoes"

	id: int = Column(Integer, primary_key = True, autoincrement=True)
	data_criacao: datetime = Column(DateTime, default=datetime.now)
	texto: str = Column(String(1000), unique  = False, nullable = False)
	assunto: str = Column(String(50), unique = False, nullable=False)

