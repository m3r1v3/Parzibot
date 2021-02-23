from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ.get('DATABASE_URL'), echo=True)
Base = declarative_base()


def create_session():
    Session = sessionmaker(bind=engine)
    return Session()


def check_user(nickname, server):
    try:
        create_session().query(UserBase).filter_by(nickname=nickname, server=server).first()
    except AttributeError:
        add_in_user_base(nickname, server)


def add_in_user_base(nickname, server):
    """Add user in db"""
    new_user = UserBase(nickname=nickname, server=server, language="EN")
    session = create_session()
    session.add(new_user)
    session.commit()


class UserBase(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    nickname = Column(String(50), unique=True, nullable=False)
    server = Column(Integer)
    language = Column(String(2))

    def __repr__(self):
        return "<UserBase(nickname='%s', server='%s', language='%s')>" % \
               (self.nickname, self.server, self.language)
