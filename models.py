from datetime import date
import enum

from pydantic import model_validator
from sqlmodel import SQLModel,Field
from typing import Optional
from sqlalchemy import Column, Integer

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
    quest_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True)
    )

    name: str = Field(nullable=False, min_length=2, max_length=100)
    time_coeff: int = Field(nullable=False, ge=1, le=10)
    difficulty_coeff: int = Field(nullable=False, ge=1, le=10)
    importance_coeff: int = Field(nullable=False, ge=1, le=10)
    arc_id : int = Field(nullable=True, foreign_key='Arcs.arc_id')
    frequency_mode: QuestFrequencyMode = Field(nullable=False, default=QuestFrequencyMode.OCCASIONAL)
    frequency: int = Field(nullable=True, ge=1, lt=7)

class QuestVersionHistory(SQLModel, table=True):
    __tablename__ = 'QuestVersionHistory'
    __table_args__ = {'extend_existing': True}

    version_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True)
    )
    quest_id: int = Field(foreign_key='Quests.quest_id', nullable=False)
    valid_before: date = Field(nullable=False)

    time_coeff: int = Field(nullable=False, ge=1, le=10)
    difficulty_coeff: int = Field(nullable=False, ge=1, le=10)
    importance_coeff: int = Field(nullable=False, ge=1, le=10)
    frequency_mode: QuestFrequencyMode = Field(nullable=False)
    frequency: int = Field(nullable=True)

# Table de validation des quêtes
class QuestValidation(SQLModel, table=True):

    __tablename__ = 'QuestValidations'
    __table_args__ = {'extend_existing': True}

    quest_id: int = Field(primary_key=True, foreign_key='Quests.quest_id')
    validation_date: date = Field(nullable=False, primary_key=True)
    xp_earned: int = Field(nullable=False, default=0)

# Table des Arcs
class Arc(SQLModel, table=True):

    __tablename__ = 'Arcs'
    __table_args__ = {'extend_existing': True}

    # Id autogénéré
    arc_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True)
    )

    name: str = Field(nullable=False, min_length=2, max_length=100, unique=True)
    description: str = Field(nullable=True, min_length=1, max_length=1000)

# Table des Paliers
class Palier(SQLModel, table=True):

    __tablename__ = 'Paliers'
    __table_args__ = {'extend_existing': True}

    # Id autogénéré
    palier_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True)
    )

    name: str = Field(nullable=False, min_length=2, max_length=100, unique=True)
    description: str = Field(nullable=True, min_length=1, max_length=1000)
    validation_date: date = Field(nullable=True)

class RewardType(enum.StrEnum):
    FREEZE = "FREEZE"
    CUSTOM = "CUSTOM"
# Table des récompenses
class Reward(SQLModel, table=True):
    __tablename__ = 'Rewards'
    __table_args__ = {'extend_existing': True}

    reward_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True)
    )
    name: str = Field(nullable=False, min_length=2, max_length=100, unique=True)
    description: Optional[str] = Field(default=None, nullable=True, min_length=1, max_length=1000)
    type: RewardType = Field(nullable=False, default=RewardType.CUSTOM)

    @model_validator(mode="after")
    def check_description_rules(self) -> "Reward":
        if self.type == RewardType.FREEZE and self.description is not None:
            raise ValueError("Une récompense FREEZE ne doit pas avoir de description.")
        if self.type == RewardType.CUSTOM and not self.description:
            raise ValueError("Une récompense CUSTOM doit avoir une description.")
        return self