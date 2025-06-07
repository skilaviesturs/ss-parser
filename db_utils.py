from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from config import DATABASE_PATH
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
                  date_removed=None    # kad vairs nav feedā
              )
              session.add(db_entry)
          else:
              # Ja sludinājums bija atzīmēts kā "noņemts", bet tagad atkal redzams
              if exists.date_removed is not None:
                  exists.date_removed = None

      try:
          session.commit()
      except IntegrityError:
          session.rollback()

