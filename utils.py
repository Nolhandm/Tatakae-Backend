from datetime import date, timedelta

from models import QuestFrequencyMode

def get_period_start(frequency_mode: QuestFrequencyMode, ref_date: date) -> date|None:
    """Renvoie la date de début de la période en fonction du mode de fréquence et d'une date de référence."""
    match frequency_mode:
        case QuestFrequencyMode.DAILY:
            return ref_date
        case QuestFrequencyMode.WEEKLY:
            return ref_date - timedelta(days=ref_date.weekday())  # Lundi de la semaine
        case QuestFrequencyMode.MONTHLY:
            return ref_date.replace(day=1)  # Premier jour du mois
        case QuestFrequencyMode.OCCASIONAL:
            return None  # Pas de période spécifique pour les quêtes occasionnelles

def get_previous_period_date(frequency_mode: QuestFrequencyMode, ref_date: date) -> date|None:
    """Renvoie la date de fin de la période précédente en fonction du mode de fréquence et d'une date de référence."""
    match frequency_mode:
        case QuestFrequencyMode.DAILY:
            return ref_date - timedelta(days=1)
        case QuestFrequencyMode.WEEKLY:
            # Obtenir le dernier jour de la semaine précédente
            first_day_of_current_week = ref_date - timedelta(days=ref_date.weekday())
            return first_day_of_current_week - timedelta(days=1)
        case QuestFrequencyMode.MONTHLY:
            # Obtenir le dernier jour du mois précédent
            first_day_of_current_month = ref_date.replace(day=1)
            return first_day_of_current_month - timedelta(days=1)
        case QuestFrequencyMode.OCCASIONAL:
            return None  # Pas de période spécifique pour les quêtes occasionnelles