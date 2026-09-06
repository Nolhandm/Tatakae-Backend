

from sqlmodel import Session, select
from models import *
from datetime import timedelta
from utils import get_period_start, get_previous_period_date

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

def check_quest(session: Session,quest_id: int, validation_date : date):
    session.add(QuestValidation(quest_id=quest_id, validation_date=validation_date))
    session.commit()
    return True

def uncheck_quest(session: Session, quest_id : int, validation_date : date):
    statement = (select(QuestValidation)
                     .where(QuestValidation.quest_id==quest_id)
                     .where(QuestValidation.validation_date==validation_date))

    val_quest = session.exec(statement).first()

    session.delete(val_quest)
    session.commit()
    return True

# ---------- Statut des quêtes --------------------

def is_frequency_reached(quest: Quest, validation_dates : set[date], ref_date: date): 
    """Vérifie si la fréquence de validation d'une quête a été atteinte pour la période de la date de référence à partir de la liste des dates de validation fournies."""

    if quest.frequency_mode == QuestFrequencyMode.OCCASIONAL:
        return ref_date in validation_dates

    start_date = get_period_start(quest.frequency_mode, ref_date)

    count = sum(1 for d in validation_dates if start_date <= d <= ref_date)
    return count >= quest.frequency

def compute_streak(quest: Quest, validation_dates: set[date], ref_date: date):
    """Calcule la série de validations consécutives pour une quête donnée à partir d'une date de référence et d'une liste de dates de validation fournies."""
    if quest.frequency_mode == QuestFrequencyMode.OCCASIONAL:
        return 0

    if ref_date > get_previous_period_date(quest.frequency_mode, date.today()) and ref_date <= date.today():
        print(quest.quest_id, "is in current period")
        # streak à partir de la période précédente si on est dans la période actuelle (qui n'est pas encore terminée).
        current_date = get_previous_period_date(quest.frequency_mode, ref_date)
        streak = 1 if is_frequency_reached(quest, validation_dates, ref_date) else 0
    else :
        print(quest.quest_id, "is NOT in current period")
        current_date = ref_date
        streak = 0

    while True:
        if is_frequency_reached(quest, validation_dates, current_date):
            streak += 1
            current_date = get_previous_period_date(quest.frequency_mode, current_date)
        else:
            break

    return streak

def get_all_quests_status_during_period(session: Session, start_date: date, end_date: date):

    statement = select(Quest)
    quests = session.exec(statement).all()

    statement = select(QuestValidation)
    validations = session.exec(statement).all()
    validations_by_quest: dict[int, set[date]] = {}
    for validation in validations:
        validations_by_quest.setdefault(validation.quest_id, set()).add(validation.validation_date)

    current_date = start_date
    result = {}

    for quest in quests:
        result[quest.quest_id] = {}
        date_set = validations_by_quest.get(quest.quest_id, set())
        while current_date <= end_date:    
            result[quest.quest_id][current_date] = {

                    "checked": current_date in date_set,
                    "frequency_reached": is_frequency_reached(quest, date_set, current_date),
                    "streak": compute_streak(quest, date_set, current_date)
            }
            current_date += timedelta(days=1)
        current_date = start_date  # Reset current_date for the next quest
    
    return result

def get_quest_status_during_period(session: Session, quest_id: int, start_date: date, end_date: date):

    statement = select(Quest).where(Quest.quest_id == quest_id)
    quest = session.exec(statement).first()

    if not quest:
        raise ValueError(f"La quête avec l'ID {quest_id} n'existe pas.")

    statement = select(QuestValidation).where(QuestValidation.quest_id == quest_id)
    validations = session.exec(statement).all()

    validations_dates = set({validation.validation_date for validation in validations})

    result = {}

    current_date = start_date
    while current_date <= end_date:
        result[current_date] = {
            "checked": current_date in validations_dates,
            "frequency_reached": is_frequency_reached(quest, validations_dates, current_date),
            "streak": compute_streak(quest, validations_dates, current_date)
        }
        current_date += timedelta(days=1)

    return result
