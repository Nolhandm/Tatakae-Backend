

from sqlmodel import Session, select
from models import *

# ---------- Accès quêtes --------------------

def get_all_quests(session:Session):
    statement = select(Quest)
    return session.exec(statement).all()

# ---------- Gestion quêtes --------------------

def create_quest(session:Session, quest:Quest):
    if quest.name.strip() == '':
        raise Exception('quest name is required')

    
    if not (QuestFrequencyMode)(quest.frequency_mode).is_valid_frequency(quest.frequency):
        raise Exception(f'frequency {quest.frequency} is not valid for frequency_mode {quest.frequency_mode}')

    session.add(quest)
    session.commit()
    session.refresh(quest)
    return quest

def delete_quest(session:Session, quest_id:int):
    quest = session.get(Quest, quest_id)
    if quest is None:
        raise ValueError(f"La quête avec l'ID {quest_id} n'existe pas.")

    # Clean the validation of the quest
    statement = select(QuestValidation).where(QuestValidation.quest_id == quest_id)
    questValidations= session.exec(statement).all()
    for validation in questValidations:
        session.delete(validation)

    # Remove the quest
    session.delete(quest)
    session.commit()
    return quest

# ----------- Validation ------------------

def get_all_checked_quests_ids_during_period(session: Session, start_date : date, end_date : date): 

    if start_date > end_date:
        raise Exception('start_date must be before end_date')

    statement = (
        select(QuestValidation)
        .where(QuestValidation.validation_date >= start_date)
        .where(QuestValidation.validation_date <= end_date)
    )

    rows = session.exec(statement).all()
    result = {}
    for questValidation in rows:
        result.setdefault(questValidation.validation_date, []).append(questValidation.quest_id)
    return result


def check_quest(session: Session,quest_id, validation_date : date):
    session.add(QuestValidation(quest_id=quest_id, validation_date=validation_date))
    session.commit()
    return True

def uncheck_quest(session: Session, quest_id, validation_date):
    statement = (select(QuestValidation)
                     .where(QuestValidation.quest_id==quest_id)
                     .where(QuestValidation.validation_date==validation_date))

    val_quest = session.exec(statement).first()

    session.delete(val_quest)
    session.commit()
    return True

