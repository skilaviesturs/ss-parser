from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, relationship
from lib.config import DATABASE_PATH
from datetime import date

Base = declarative_base()

class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String, unique=True)
    published = Column(String)
    is_processed = Column(Boolean, default=False)
    is_match = Column(Boolean, default=False)
    location = Column(String, nullable=True)
    region = Column(String, nullable=True)
    street = Column(String, nullable=True)
    building_type = Column(String, nullable=True)
    rooms = Column(Integer, nullable=True)
    floor = Column(Integer, nullable=True)
    area = Column(Float, nullable=True)
    price = Column(Integer, nullable=True)
    price_m2 = Column(Float, nullable=True)
    date_published = Column(Date, nullable=True)
    hash = Column(String, nullable=True, index=True)

class MonitoredFlat(Base):
    __tablename__ = 'monitored_flats'

    hash = Column(String, primary_key=True)
    location = Column(String)
    region = Column(String)
    street = Column(String)
    building_type = Column(String)
    rooms = Column(Integer)
    floor = Column(Integer)
    area = Column(Float)
    link = Column(String)
    price = Column(Integer)
    created_at = Column(Date, default=date.today)

class FlatPriceHistory(Base):
    __tablename__ = 'flat_price_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    flat_hash = Column(String, ForeignKey('monitored_flats.hash'))
    date = Column(Date, default=date.today)
    price = Column(Integer)

    flat = relationship("MonitoredFlat", backref="price_history")

engine = create_engine(
    DATABASE_PATH,
    pool_size=5,        # default ir 5, bet vari palielināt ja vajag
    max_overflow=10,    # cik pagaidu savienojumi var būt virs baseina
    pool_timeout=30     # pēc cik sekundēm mest TimeoutError, ja nav brīva savienojuma
)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_entries_to_db(entries):
    with Session() as session:
      for entry in entries:
          exists = session.query(Entry).filter_by(link=entry.get('link')).first()
          if not exists:
              db_entry = Entry(
                  title=entry.get('title'),
                  link=entry.get('link'),
                  published=entry.get('published'),
                  is_processed=False,
                  location=entry.get('location'),
                  building_type=entry.get('building_type'),
                  rooms=entry.get('rooms'),
                  floor=entry.get('floor'),
                  area=entry.get('area'),
                  price=entry.get('price'),
                  price_m2=entry.get('price_m2'),
                  street=entry.get('street'),
                  date_published=date.today(), # kad pirmais reizi parādās feedā
                  hash=entry.get('hash', None)  # ja ir hash, tad pievieno
              )
              session.add(db_entry)

      try:
          session.commit()
      except IntegrityError:
          session.rollback()

def update_price_history(session, flat: MonitoredFlat, new_price: int):
    # Tikai ja cena ir mainījusies
    if flat.price != new_price:
        flat.price = new_price
        history_entry = FlatPriceHistory(
            flat_hash=flat.hash,
            date=date.today(),
            price=new_price
        )
        session.add(history_entry)
