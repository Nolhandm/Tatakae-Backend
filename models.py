from datetime import date

from sqlmodel import SQLModel,Field
from typing import Optional

# Table des Quêtes
class Quest(SQLModel, table=True):

    __tablename__ = 'Quests'
    __table_args__ = {'extend_existing': True}

    # Id autogénéré
    quest_id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(nullable=False, min_length=2, max_length=100)
    time_coeff: int = Field(nullable=False, ge=1, le=10)
    difficulty_coeff: int = Field(nullable=False, ge=1, le=10)
    importance_coeff: int = Field(nullable=False, ge=1, le=10)

# Table de validation
class QuestValidation(SQLModel, table=True):

    __tablename__ = 'QuestValidations'
    __table_args__ = {'extend_existing': True}

    quest_id: int = Field(primary_key=True, foreign_key='Quests.quest_id')
    validation_date: date = Field(nullable=False, primary_key=True)