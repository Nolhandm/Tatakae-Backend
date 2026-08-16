from datetime import date
import enum

from sqlmodel import SQLModel,Field
from typing import Optional

class QuestFrequencyMode(enum.StrEnum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    OCCASIONAL = "OCCASIONAL"

    def is_valid_frequency(self, value: int) -> bool:

        match self:
            case QuestFrequencyMode.DAILY:
                return value == 1
            case QuestFrequencyMode.WEEKLY:
                return value >= 1 and value < 7
            case QuestFrequencyMode.MONTHLY:    
                return value >= 1 and value < 5
            case QuestFrequencyMode.OCCASIONAL:
                return value == 0
            

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
    arc_id : int = Field(nullable=True, foreign_key='Arcs.arc_id')
    frequency_mode: QuestFrequencyMode = Field(nullable=False, default=QuestFrequencyMode.OCCASIONAL)
    frequency: int = Field(nullable=True, ge=1, lt=7)

# Table de validation des quêtes
class QuestValidation(SQLModel, table=True):

    __tablename__ = 'QuestValidations'
    __table_args__ = {'extend_existing': True}

    quest_id: int = Field(primary_key=True, foreign_key='Quests.quest_id')
    validation_date: date = Field(nullable=False, primary_key=True)

class Arc(SQLModel, table=True):

    __tablename__ = 'Arcs'
    __table_args__ = {'extend_existing': True}

    # Id autogénéré
    arc_id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(nullable=False, min_length=2, max_length=100, unique=True)
    description: str = Field(nullable=True, min_length=1, max_length=1000)
