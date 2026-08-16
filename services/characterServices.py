from sqlalchemy import func
from sqlmodel import Session, select
from models import *
from math import sqrt, pow, floor
from config import *

#========================
# Statistiques du joueur
#========================

def compute_total_xp_cumulated(session: Session):
    # Get number of checks for each quest
    statement = (select(Quest, func.count().label('total'))
                     .join(QuestValidation, QuestValidation.quest_id == Quest.quest_id)
                     .group_by(Quest.quest_id))
    result = session.exec(statement).all()

    total_xp_cumulated = 0
    for hab in result:
        total_xp_cumulated += hab[1] * QUEST_BASE_XP * (hab[0].time_coeff + hab[0].difficulty_coeff + hab[0].importance_coeff)
    return total_xp_cumulated

def compute_actual_level(session: Session):

    total_xp_cumulated = compute_total_xp_cumulated(session)

    actual_level = (LEVEL_INCREASE_XP / 2 - LEVEL_BASE_XP + sqrt(pow(LEVEL_BASE_XP - LEVEL_INCREASE_XP / 2, 2) + 2 * LEVEL_INCREASE_XP * total_xp_cumulated)) / LEVEL_INCREASE_XP + 1

    return int(actual_level)

def compute_actual_rank(session: Session):

    actual_level = compute_actual_level(session)
    return floor(actual_level / (MAX_LEVEL/ RANK_NUMBER))

# Remis à zéro à chaque passage de niveau, correspond à l'xp pour ce niveau précis
def compute_actual_xp(session : Session):

    total_xp_cumulated = compute_total_xp_cumulated(session)
    actual_level = compute_actual_level(session)

    total_xp_needed_for_actual_level = compute_xp_cumulated_needed_to_reach_level_x(actual_level)

    return total_xp_cumulated - total_xp_needed_for_actual_level

def compute_xp_needed_to_finish_actual_level(session: Session):
    actual_level = compute_actual_level(session)

    return compute_xp_needed_to_finish_level_x(actual_level)

#=========================
# Fonctions de calcul
#=========================

def compute_xp_cumulated_needed_to_finish_level_x(level: int):
    if level < 0:
        raise Exception('Level cannot be negative')
    if level == 0:
        return 0
    return int(level * LEVEL_BASE_XP + (pow(level,2) - level)*LEVEL_INCREASE_XP/2)

def compute_xp_cumulated_needed_to_reach_level_x(level: int):
    if level <= 0:
        raise Exception('Level cannot be negative or null')
    return compute_xp_cumulated_needed_to_finish_level_x(level-1)

def compute_xp_needed_to_finish_level_x(level:int):
    if level <= 0:
        raise Exception('Level cannot be negative or null')
    return int(LEVEL_BASE_XP + (level - 1) * LEVEL_INCREASE_XP)

