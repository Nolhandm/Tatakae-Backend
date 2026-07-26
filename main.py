from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from services.habitsService import *


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
