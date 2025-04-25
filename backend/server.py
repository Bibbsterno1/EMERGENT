
from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import uvicorn
import uuid
import logging
from pathlib import Path
import httpx
from datetime import datetime

# /backend 
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'hubspot_integration')]

app = FastAPI(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Models
class NewsItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    headline: str
    source: str
    date: str
    quirkFactor: int = Field(ge=1, le=5)
    summary: str
    sentiment: str
    url: str

class CompanyInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    industry: Optional[str] = None
    quirkNews: List[NewsItem] = []

# Initialization - create collections if they don't exist
@app.on_event("startup")
async def startup_db_client():
    try:
        # Check if collections exist, if not create them
        collections = await db.list_collection_names()
        if "companies" not in collections:
            await db.create_collection("companies")
        if "news_items" not in collections:
            await db.create_collection("news_items")
        logger.info("Database collections initialized")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

# Sample data for testing
SAMPLE_COMPANIES = [
    CompanyInfo(
        name="Acme Corporation",
        industry="Technology",
        quirkNews=[
            NewsItem(
                headline="Acme CEO Starts Office Alpaca Farm to 'Boost Morale'",
                source="Tech Daily",
                date="March 15, 2025",
                quirkFactor=4,
                summary="In an unusual workplace initiative, Acme's CEO has introduced a herd of alpacas to company headquarters, claiming they improve creativity and reduce stress.",
                sentiment="😂",
                url="#"
            ),
            NewsItem(
                headline="Acme's AI Assistant Accidentally Orders 10,000 Rubber Ducks",
                source="Business Insider",
                date="March 10, 2025",
                quirkFactor=5,
                summary="A glitch in Acme's new AI procurement system resulted in thousands of rubber ducks being delivered to their main office. Employees have turned it into an impromptu charity drive.",
                sentiment="😮",
                url="#"
            )
        ]
    ),
    CompanyInfo(
        name="Globex Corporation",
        industry="Manufacturing",
        quirkNews=[
            NewsItem(
                headline="Globex Introduces 'Casual Tuxedo Fridays'",
                source="Business Fashion Weekly",
                date="March 12, 2025",
                quirkFactor=3,
                summary="In a twist on casual Fridays, Globex now requires employees to wear tuxedos and evening gowns, but in a 'casual way' each Friday.",
                sentiment="🤔",
                url="#"
            )
        ]
    )
]

# Routes
@app.get("/")
async def root():
    return {"message": "HubSpot Quirky News Integration API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/companies")
async def get_companies():
    """Get a list of all companies"""
    try:
        companies = await db.companies.find().to_list(length=100)
        if not companies:
            # Return sample data if no companies in DB
            return SAMPLE_COMPANIES
        return companies
    except Exception as e:
        logger.error(f"Error fetching companies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/company-info")
async def get_company_info(name: str = Query(..., description="Company name")):
    """Get information for a specific company"""
    try:
        company = await db.companies.find_one({"name": name})
        if not company:
            # Return sample data if company not found
            for sample_company in SAMPLE_COMPANIES:
                if sample_company.name == name:
                    return sample_company
            # If not found in samples either, return 404
            raise HTTPException(status_code=404, detail=f"Company {name} not found")
        return company
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching company {name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/company-info")
async def create_company(company: CompanyInfo):
    """Create a new company entry"""
    try:
        company_dict = company.dict()
        result = await db.companies.insert_one(company_dict)
        if result.inserted_id:
            return {"id": str(result.inserted_id), **company_dict}
        else:
            raise HTTPException(status_code=500, detail="Failed to create company")
    except Exception as e:
        logger.error(f"Error creating company: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# This endpoint will be connected to a news API in the full implementation
@app.get("/api/quirky-news")
async def get_quirky_news(company_name: str = Query(..., description="Company name")):
    """Get quirky news for a company - currently returns sample data"""
    try:
        # In a real implementation, this would connect to a news API
        # and filter for quirky/amusing news about the company
        for company in SAMPLE_COMPANIES:
            if company.name == company_name:
                return {"news": company.quirkNews}
        
        # If company not found in samples, return empty list
        return {"news": []}
    except Exception as e:
        logger.error(f"Error fetching quirky news: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# HubSpot specific endpoints - would be implemented with actual HubSpot SDK
@app.get("/api/hubspot/setup")
async def hubspot_setup():
    """Get HubSpot setup information"""
    return {
        "isConfigured": False,
        "authUrl": "https://app.hubspot.com/oauth/authorize?client_id=YOUR_CLIENT_ID&scope=contacts&redirect_uri=YOUR_REDIRECT_URI"
    }

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
