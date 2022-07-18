import os

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://"))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role_id = Column(String(50), unique=True, nullable=False)
    server = Column(String(30), unique=True, nullable=False)

    @staticmethod
    def add(role_id, server: str):
        """Add user in db"""
        session.add(Role(role_id=role_id, server=str(server))).commit()

    @staticmethod
    def get_role(server: str):
        try:
            return session.query(Role).filter_by(server=str(server)).first().role_id
        except AttributeError: return None

    @staticmethod
    def delete(server: str):
        session.delete(session.query(Role).filter_by(server=str(server)).first()).commit()

    def __repr__(self):
        return "<Role(id='%s', role_id='%s', server='%s')>" % (self.id, self.role_id, self.server)