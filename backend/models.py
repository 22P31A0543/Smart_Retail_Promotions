from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    SKU = Column(String, primary_key=True, index=True)
    ProductName = Column(String, nullable=False)
    Price = Column(Float, nullable=False)
    ImageURL = Column(String)

class Campaign(Base):
    __tablename__ = "campaigns"
    CampaignID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Name = Column(String, nullable=False)
    Description = Column(String)
    StartDate = Column(Date)
    EndDate = Column(Date)
    DiscountType = Column(String)
    DiscountValue = Column(Float)
    Status = Column(String)

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
