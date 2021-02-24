import os

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get('DATABASE_URL'))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


def check_user(nickname, server: str):
    try:
        session.query(User).filter_by(nickname=nickname, server=str(server)).first()
    except AttributeError:
        add_in_user_base(nickname, str(server))


def add_in_user_base(nickname, server: str, language="EN"):
    """Add user in db"""
    new_user = User(nickname=nickname, server=str(server), language=language)
    session.add(new_user)
    session.commit()


def delete(nickname, server: str):
    session.delete(session.query(User).filter_by(nickname=nickname, server=str(server)).first())
    session.commit()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    nickname = Column(String(50), unique=True, nullable=False)
    server = Column(String(30))
    language = Column(String(50))

    def __repr__(self):
        return "<User(id='%s', nickname='%s', server='%s', language='%s')>" % (
            self.user_id, self.nickname, self.server, self.language)
