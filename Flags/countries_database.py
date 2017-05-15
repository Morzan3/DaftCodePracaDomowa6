from sqlalchemy import (
    Table,
    Column,
    Integer,
    Numeric,
    String,
    DateTime,
    ForeignKey,
    create_engine,
    select
)
from sqlalchemy.orm import (
    relationship,
)

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import as_declarative

import os.path
engine = create_engine('sqlite:///countries.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@as_declarative()
class Base():
    pass


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer(), primary_key=True)
    ckey = Column(String(), nullable=True)
    flag = Column(String(), nullable=True)


def create_db():
    if not os.path.exists('./countries.db'):
        Base.metadata.create_all(engine)


create_db()