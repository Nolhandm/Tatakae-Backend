from datetime import date

from sqlmodel import SQLModel,Field
from typing import Optional

# Table des Habitudes
class Habit(SQLModel, table=True):

    __tablename__ = 'Habits'
    __table_args__ = {'extend_existing': True}

    # Id autogénéré
    habit_id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(nullable=False, min_length=2, max_length=100)
    time_coeff: int = Field(nullable=False, ge=1, le=10)
    difficulty_coeff: int = Field(nullable=False, ge=1, le=10)
    importance_coeff: int = Field(nullable=False, ge=1, le=10)

# Table de validation
class Validation_habits(SQLModel, table=True):


    __tablename__ = 'Validation_habits'
    __table_args__ = {'extend_existing': True}

    habit_id: int = Field(primary_key=True, foreign_key='Habits.habit_id')
    validation_date: date = Field(nullable=False, primary_key=True)