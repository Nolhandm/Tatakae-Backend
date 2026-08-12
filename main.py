from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
import services.questsService as questService
import services.statsServices as statsService
from sqlmodel import Session


# Needed so the tables can be generated
from models import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Indispensable pour que ton front Vue (autre port/domaine) puisse appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # l'URL de ton dev server Vite
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# /quests routes
# ==========================

@app.get("/quests")
def get_all_quests(session: Session = Depends(get_session)):
    return questService.get_all_quests(session)

@app.post("/quests")
def create_quest(quest: Quest, session: Session = Depends(get_session)):
    questService.create_quest(session, quest)
    return 200

@app.get("/quests/checked")
def get_all_checked_quests_ids_at_date(validation_date: date, session: Session = Depends(get_session)):
    return questService.get_all_checked_quests_ids_at_date(session, validation_date)

@app.post("/quests/{quest_id}/check")
def check_quest(quest_id: int, validation_date: date, session: Session = Depends(get_session)):
    return questService.check_quest(session, quest_id, validation_date)

@app.post("/quests/{quest_id}/uncheck")
def uncheck_quest(quest_id: int, validation_date: date, session: Session = Depends(get_session)):
    return questService.uncheck_quest(session, quest_id, validation_date)

@app.delete("/quests/{quest_id}")
def delete_quest(quest_id: int, session: Session = Depends(get_session)):
    try:
        questService.delete_quest(session, quest_id)
        return 200
    except ValueError:
        return 404

# ==========================
# /character routes
# ==========================

@app.get("/character/stats")
def get_character_stats(session: Session = Depends(get_session)):
    total_xp = statsService.get_total_xp(session)
    level = statsService.compute_level(session)
    cumul_xp_previous_level = statsService.compute_cumul_xp_for_level(level - 1)
    xp_needed_this_level = statsService.compute_xp_for_level(level)
    rank = statsService.compute_rank()

    return {
        "total_xp": total_xp,
        "level": level,
        "current_xp_in_level": total_xp - cumul_xp_previous_level,
        "xp_needed_this_level": xp_needed_this_level,
        "rank": rank
    }
