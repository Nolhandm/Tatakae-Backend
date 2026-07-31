from sqlmodel import Session, select
from models import *

# ---------- Gestion habitudes --------------------
'''def add_new_habit(session:Session, name, time_coeff, difficulty_coeff, importance_coeff):
    if name.strip() == '':
        return
    habit = Habit(
        name=name,
        time_coeff=time_coeff,
        difficulty_coeff=difficulty_coeff,
        importance_coeff=importance_coeff)

    session.add(habit)
    session.commit()'''

def add_new_habit(session:Session, habit:Habit):
    if habit.name.strip() == '':
        return

    session.add(habit)
    session.commit()

def get_all_habits(session:Session):
    statement = select(Habit)
    return session.exec(statement).all()

# ----------- Validation ------------------

def get_all_checked_habit_ids(session: Session, validation_date : date):

    statement = select(Validation_habits.habit_id).where(Validation_habits.validation_date == validation_date)
    return session.exec(statement).all()


def check_habit(session: Session,habit_id, validation_date : date):
    session.add(Validation_habits(habit_id=habit_id, validation_date=validation_date))
    session.commit()

def uncheck_habit(session: Session, habit_id, validation_date):
    statement = (select(Validation_habits)
                     .where(Validation_habits.habit_id==habit_id)
                     .where(Validation_habits.validation_date==validation_date))

    val_habit = session.exec(statement).first()

    session.delete(val_habit)
    session.commit()