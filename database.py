import os

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get('DATABASE_URL'))
Base = declarative_base()


def create_session():
    Session = sessionmaker(bind=engine)
    return Session()


def check_user(nickname, server: str):
    try:
        create_session().query(User).filter_by(nickname=nickname, server=server).first()
    except AttributeError:
        add_in_user_base(nickname, server)


def add_in_user_base(nickname, server: str, language="EN"):
    """Add user in db"""
    new_user = User(nickname=nickname, server=server, language=language)
    session = create_session()
    session.add(new_user)
    session.commit()


def delete(nickname, server):
    session = create_session()
    session.query(User).filter_by(nickname=nickname, server=server).first().delete()
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
