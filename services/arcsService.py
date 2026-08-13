from sqlmodel import Session, select
from models import *

# ---------- Accès arcs --------------------

def get_all_arcs(session:Session):
    statement = select(Arc)
    return session.exec(statement).all()

# ---------- Gestion arcs --------------------

def create_arc(session:Session, arc:Arc):
    if arc.name.strip() == '':
        raise Exception('Arc name is required')

    # name should be unique
    statement = select(Arc).where(Arc.name == arc.name)
    res = session.exec(statement).first()
    if res is not None:
        raise Exception('Arc already exists')

    session.add(arc)
    session.commit()
    session.refresh(arc)
    return arc