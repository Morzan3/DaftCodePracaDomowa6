from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
)

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import as_declarative

import os.path
engine = create_engine('sqlite:///strings.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@as_declarative()
class Base():
    pass


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer(), primary_key=True)
    en_US = Column(String(), nullable=True)
    pl_Pl = Column(String(), nullable=True)
    skey = Column(String(), nullable=True)


def create_db():
    if not os.path.exists('./strings.db'):
        Base.metadata.create_all(engine)


create_db()