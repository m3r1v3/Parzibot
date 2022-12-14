import os
import random

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get('DATABASE_URL'))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    role = Column(String(50), unique=True, nullable=False)
    server = Column(String(30), unique=True, nullable=False)

    @staticmethod
    def add(role: str, server: str):
        session.add(Role(id=random.randint(1, 2147483647), role=role, server=server))
        session.commit()

    @staticmethod
    def get_role(server: str):
        try:
            return session.query(Role).filter_by(server=server).first().role
        except AttributeError: return None

    @staticmethod
    def delete(server: str):
        session.delete(session.query(Role).filter_by(server=server).first())
        session.commit()

    def __repr__(self):
        return "<Role(id='%s', role='%s', server='%s')>" % (self.id, self.role, self.server)
