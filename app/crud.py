from sqlalchemy.orm import Session

from . import models, schemas


def get_all_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()