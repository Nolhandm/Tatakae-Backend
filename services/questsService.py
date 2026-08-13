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

def get_all_checked_quests_ids_at_date(session: Session, validation_date : date):

    statement = select(QuestValidation.quest_id).where(QuestValidation.validation_date == validation_date)
    return session.exec(statement).all()


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