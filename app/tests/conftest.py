import os
from typing import List
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from fastapi.testclient import TestClient
from app.backend.api import app

from app.backend.models import User, Post


def fill_data(db: Session, user, post):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user is None:
        db.add(user)
    
    db_post = db.query(Post).filter(Post.title == post.title).first()
    if db_post is None:
        db.add(post)

    db.commit()


@pytest.fixture(scope='module')
def setup_db():
    try:
        engine = create_engine(
            "sqlite:///./test.db", connect_args={"check_same_thread": False}
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        Base = declarative_base()
        Base.metadata.create_all(engine)

        user = User(username='admin', password='admin')
        post = Post(title='first', text='qwerty')

        fill_data(db, user, post)

        yield db
    finally:
        db.close()


@pytest.fixture()
def client(setup_db):
    with TestClient(app) as test_client:
        yield test_client
