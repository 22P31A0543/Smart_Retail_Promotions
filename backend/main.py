
from fastapi import FastAPI, Depends, HTTPException, Header, Response
from fastapi.middleware.cors import CORSMiddleware
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from models import Product, Campaign, SessionLocal, Base
from pydantic import BaseModel


API_KEY = "mysecretapikey"  # Change this to a secure value in production

app = FastAPI()

# Enable CORS for all origins (customize as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class ProductCreate(BaseModel):
    SKU: str
    ProductName: str
    Price: float
    ImageURL: str = None

class ProductOut(ProductCreate):
    class Config:
        orm_mode = True

class CampaignCreate(BaseModel):
    Name: str
    Description: str = None
    StartDate: date = None
    EndDate: date = None
    DiscountType: str = None
    DiscountValue: float = None
    Status: str = None

class CampaignOut(CampaignCreate):
    CampaignID: int
    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Product Endpoints
@app.post("/products/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    try:
        db.commit()
        db.refresh(db_product)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Product with this SKU may already exist.")
    return db_product

@app.get("/products/", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# CRUD for Campaigns (secured with API key)
@app.post("/campaigns/", response_model=CampaignOut, dependencies=[Depends(verify_api_key)])
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    db_campaign = Campaign(**campaign.dict())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

@app.get("/campaigns/", response_model=List[CampaignOut], dependencies=[Depends(verify_api_key)])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).all()

@app.get("/campaigns/{campaign_id}", response_model=CampaignOut, dependencies=[Depends(verify_api_key)])
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.CampaignID == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@app.put("/campaigns/{campaign_id}", response_model=CampaignOut, dependencies=[Depends(verify_api_key)])
def update_campaign(campaign_id: int, campaign: CampaignCreate, db: Session = Depends(get_db)):
    db_campaign = db.query(Campaign).filter(Campaign.CampaignID == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    for key, value in campaign.dict().items():
        setattr(db_campaign, key, value)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

@app.delete("/campaigns/{campaign_id}", dependencies=[Depends(verify_api_key)])
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = db.query(Campaign).filter(Campaign.CampaignID == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(db_campaign)
    db.commit()
    return {"detail": "Campaign deleted"}

# Publish Campaign endpoint
@app.post("/publishCampaign/{campaign_id}", dependencies=[Depends(verify_api_key)])
def publish_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = db.query(Campaign).filter(Campaign.CampaignID == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db_campaign.Status = "Live"
    db.commit()
    db.refresh(db_campaign)
    # Generate mock public URL
    public_url = f"https://mockcampaigns.com/campaign/{campaign_id}"
    return {"detail": "Campaign published", "public_url": public_url}

# QR Code endpoint for campaign public URL
@app.get("/campaigns/{campaign_id}/qrcode", dependencies=[Depends(verify_api_key)])
def get_campaign_qrcode(campaign_id: int, db: Session = Depends(get_db)):
    public_url = f"https://mockcampaigns.com/campaign/{campaign_id}"
    img = qrcode.make(public_url)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
