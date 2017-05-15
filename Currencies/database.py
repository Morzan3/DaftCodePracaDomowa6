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
engine = create_engine('sqlite:///currencies.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@as_declarative()
class Base():
    pass


class Rate(Base):
    __tablename__ = 'rates'

    id = Column(Integer(), primary_key=True)
    buy_price = Column(Integer(), nullable=False)
    sell_price = Column(Integer(), nullable=False)
    trading_date = Column(DateTime(), nullable=False)
    currency_id = Column(
        Integer,
        ForeignKey('currencies.id'),
        nullable=False,
        index=True,
    )

    currency = relationship(
        'Currency',
        backref='currencies',
    )

class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer(), primary_key=True)
    full_name = Column(String(), nullable=False)
    code = Column(String(), nullable=False)

def create_db():
    if not os.path.exists('./currencies.db'):
        Base.metadata.create_all(engine)

def add_rate(rate_data, date_time):
    for single_rate in rate_data:
        currency = session.query(Currency).filter(Currency.code == single_rate['code']).first()
        if not currency:
            session.add(Currency(full_name=single_rate['currency'], code=single_rate['code']))
            session.commit()
        currency_with_code = session.query(Currency).filter(Currency.code == single_rate['code']).first()
        session.add(Rate(buy_price=single_rate['bid'], sell_price=single_rate['ask'], trading_date = date_time, currency_id = currency_with_code.id))
        session.commit()

create_db()