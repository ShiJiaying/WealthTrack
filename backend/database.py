from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./celebrity_tracker.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class NewsItem(Base):
    __tablename__ = "news_items"
    
    id = Column(Integer, primary_key=True, index=True)
    figure_name = Column(String, index=True)
    title = Column(String)
    content = Column(Text)
    source = Column(String)
    url = Column(String)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, index=True)
    figure_name = Column(String)
    summary = Column(Text)
    financial_impact = Column(Text)
    affected_sectors = Column(String)
    impact_score = Column(Float)
    recommendation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
