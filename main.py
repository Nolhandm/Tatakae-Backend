from fastapi import HTTPException, status

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
import services.questsService as questService
import services.characterServices as characterService
import services.arcsService as arcsService
from sqlmodel import Session
from dataclasses import dataclass

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
    try :
        return questService.create_quest(session, quest)
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/quests/{quest_id}/check")
def check_quest(quest_id: int, validation_date: date, session: Session = Depends(get_session)):
    return questService.check_quest(session, quest_id, validation_date)

@app.post("/quests/{quest_id}/uncheck")
def uncheck_quest(quest_id: int, validation_date: date, session: Session = Depends(get_session)):
    return questService.uncheck_quest(session, quest_id, validation_date)

@app.delete("/quests/{quest_id}")
def delete_quest(quest_id: int, session: Session = Depends(get_session)):
    try:
        return questService.delete_quest(session, quest_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/quests/status")
def get_all_quests_status_during_period(start_date: date, end_date: date, session: Session = Depends(get_session)):
    try:
        return questService.get_all_quests_status_during_period(session, start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) 

@app.get("/quests/{quest_id}/status")
def get_quest_status_during_period(quest_id: int, start_date: date, end_date: date, session: Session = Depends(get_session)):
    try:
        return questService.get_quest_status_during_period(session, quest_id, start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))    

# ==========================
# /arcs routes
# ==========================

@app.get("/arcs")
def get_all_arcs(session: Session = Depends(get_session)):
    return arcsService.get_all_arcs(session)

@app.post("/arcs")
def create_arc(arc: Arc, session: Session = Depends(get_session)):
    try:
        return arcsService.create_arc(session, arc)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# ==========================
# /character routes
# ==========================

@app.get("/character/stats")
def get_character_stats(session: Session = Depends(get_session)):

    return {
        "actual_level": characterService.compute_actual_level(session),
        "actual_rank": characterService.compute_actual_rank(session),
        "actual_xp": characterService.compute_actual_xp(session),
        "xp_needed": characterService.compute_xp_needed_to_finish_actual_level(session),
        "total_xp_cumulated": characterService.compute_total_xp_cumulated(session)
    }
