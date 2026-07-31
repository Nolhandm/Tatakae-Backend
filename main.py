from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from services.habitsService import *
from services.statsServices import get_total_xp, compute_level, compute_cumul_xp_for_level, compute_xp_for_level, compute_rank


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

@app.get("/habits")
def read_habits(session: Session = Depends(get_session)):
    return get_all_habits(session)

@app.post("/habits/create")
def create_habits(habit: Habit, session: Session = Depends(get_session)):
    add_new_habit(session, habit)
    return 200

@app.get("/habits/checked")
def read_checked_habits(validation_date: date, session: Session = Depends(get_session)):
    return get_all_checked_habit_ids(session, validation_date)

@app.post("/habits/{habit_id}/check")
def validate_habit(habit_id: int, validation_date: date, session: Session = Depends(get_session)):
    return check_habit(session, habit_id, validation_date)

@app.delete("/habits/{habit_id}/check")
def unvalidate_habit(habit_id: int, validation_date: date, session: Session = Depends(get_session)):
    uncheck_habit(session, habit_id, validation_date)
    return {"ok": True}

@app.get("/character/stats")
def get_character_stats(session: Session = Depends(get_session)):
    total_xp = get_total_xp(session)
    level = compute_level(session)
    cumul_xp_previous_level = compute_cumul_xp_for_level(level - 1)
    xp_needed_this_level = compute_xp_for_level(level)
    rank = compute_rank()

    return {
        "total_xp": total_xp,
        "level": level,
        "current_xp_in_level": total_xp - cumul_xp_previous_level,
        "xp_needed_this_level": xp_needed_this_level,
        "rank": rank
    }
