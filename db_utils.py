from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = 'sqlite:///ss_entries.db'
Base = declarative_base()

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    published = Column(String)
    is_processed = Column(Boolean, default=False)
    is_match = Column(Boolean, default=None)
    location = Column(String, default=None)
    building_type = Column(String, default=None)
    rooms = Column(Integer, default=None)
    floor = Column(Integer, default=None)
    area = Column(Float, default=None)
    price = Column(Float, default=None)

engine = create_engine(DB_PATH)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_entries_to_db(entries):
    session = Session()
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
                price=entry.get('price')
            )
            session.add(db_entry)
    session.commit()
    session.close()
