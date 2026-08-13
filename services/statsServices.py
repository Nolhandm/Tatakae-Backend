from sqlalchemy import func
from sqlmodel import Session, select
from models import *
from math import sqrt, pow, floor

# Calculer l'XP pour un jour et ajouter 10% de cette valeur à chaque niveau, on arrivera à un niveau final environ 10 fois supérieur à celui de base et on devrait arriver au niv 100 au bout de 500j

QUEST_BASE_XP = 1
LEVEL_BASE_XP = 1000
LEVEL_INCREASE_XP = LEVEL_BASE_XP * 0.1
MAX_LEVEL = 100

RANK_NUMBER = 23

def get_total_xp(session: Session):
    # Get number of checks for each quest
    statement = (select(Quest, func.count().label('total'))
                     .join(QuestValidation, QuestValidation.quest_id == Quest.quest_id)
                     .group_by(Quest.quest_id))
    result = session.exec(statement).all()

    final_xp = 0
    for hab in result:
        final_xp += QUEST_BASE_XP * hab[1] * (hab[0].time_coeff + hab[0].difficulty_coeff + hab[0].importance_coeff)
    return final_xp

def compute_level(session: Session):

    cumul = get_total_xp(session)
    level = (LEVEL_INCREASE_XP / 2 - LEVEL_BASE_XP + sqrt(pow(LEVEL_BASE_XP - LEVEL_INCREASE_XP / 2, 2) + 2 * LEVEL_INCREASE_XP * cumul)) / LEVEL_INCREASE_XP + 1

    return int(level)

def compute_cumul_xp_for_level(level):
    if level <= 0:
        return 0
    return int(LEVEL_INCREASE_XP / 2 * pow(level, 2) + (LEVEL_BASE_XP - LEVEL_INCREASE_XP / 2) * level)

def compute_xp_for_level(level):
    if level <= 0:
        return 0
    return int(LEVEL_BASE_XP + (level - 1) * LEVEL_INCREASE_XP)

def compute_rank(level):

    return floor(level / (MAX_LEVEL/ RANK_NUMBER))
