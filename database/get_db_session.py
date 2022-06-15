from sqlalchemy.orm import Session

from .database import DB


def get_db() -> Session:
    db = DB.SessionLocal()
    try:
        return db
    finally:
        db.close()
