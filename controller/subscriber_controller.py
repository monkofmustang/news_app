from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.db_connection import get_db
from models.subscribers import Subscribers, SubscriberCreate, SubscriberResponse

router = APIRouter(
    prefix="/subscribers",  # All routes will be prefixed with /subscribers
    tags=["Subscribers"],  # Tag for grouping in the documentation
)


@router.get("/", response_model=list[SubscriberResponse])
async def get_subscribers(db: Session = Depends(get_db)):
    """Get all subscribers"""
    subscribers = db.query(Subscribers).all()
    return subscribers


@router.post("/", response_model=SubscriberResponse)
async def create_subscriber(subscriber: SubscriberCreate, db: Session = Depends(get_db)):
    """Create a new subscriber"""
    # Check if the subscriber already exists
    existing_subscriber = db.query(Subscribers).filter(Subscribers.mobNumber == subscriber.mobNumber).first()
    if existing_subscriber:
        raise HTTPException(status_code=400, detail="Subscriber already exists.")
    
    # Create new subscriber
    db_subscriber = Subscribers(
        name=subscriber.name,
        mobNumber=subscriber.mobNumber,
        state=subscriber.state
    )
    
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    
    return db_subscriber


@router.get("/{subscriber_id}", response_model=SubscriberResponse)
async def get_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    """Get a specific subscriber by ID"""
    subscriber = db.query(Subscribers).filter(Subscribers.id == subscriber_id).first()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found.")
    return subscriber


@router.delete("/{subscriber_id}")
async def delete_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    """Delete a subscriber by ID"""
    subscriber = db.query(Subscribers).filter(Subscribers.id == subscriber_id).first()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found.")
    
    db.delete(subscriber)
    db.commit()
    
    return {"message": "Subscriber deleted successfully."}
