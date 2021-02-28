import os

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get('DATABASE_URL'))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    nickname = Column(String(50), unique=True, nullable=False)
    server = Column(String(30), nullable=False)
    language = Column(String(50))

    def __repr__(self):
        return "<User(user_id='%s', nickname='%s', server='%s', language='%s')>" % (
            self.user_id, self.nickname, self.server, self.language)

    def check_user(self, nickname, server: str):
        try:
            session.query(User).filter_by(nickname=nickname, server=str(server)).first()
        except AttributeError:
            self.add(nickname, str(server))

    @staticmethod
    def add(nickname, server: str, language="EN"):
        """Add user in db"""
        new_user = User(nickname=nickname, server=str(server), language=language)
        session.add(new_user)
        session.commit()

    @staticmethod
    def delete(nickname, server: str):
        session.delete(session.query(User).filter_by(nickname=nickname, server=str(server)).first())
        session.commit()


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    role_id = Column(String(50), unique=True, nullable=False)
    server = Column(String(30), unique=True, nullable=False)

    @staticmethod
    def add(role_id, server: str):
        """Add user in db"""
        new_role = Role(role_id=role_id, server=str(server))
        session.add(new_role)
        session.commit()

    @staticmethod
    def get_role(server: str):
        return session.query(Role).filter_by(server=str(server)).first().role_id

    @staticmethod
    def delete(role_id, server: str):
        session.delete(session.query(Role).filter_by(role_id=role_id, server=str(server)).first())
        session.commit()

    def __repr__(self):
        return "<Role(id='%s', role_id='%s', server='%s')>" % (
            self.id, self.role_id, self.server)
