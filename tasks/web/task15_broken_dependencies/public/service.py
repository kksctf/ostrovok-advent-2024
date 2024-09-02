#!/usr/bin/env python3

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger
import schedule
import missingpackage
from pydantic import BaseModel, validator

# Database setup
DATABASE_URL = "sqlite:///hotel_management.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RoomModel(Base):
    __tablename__ = 'rooms'
    room_number = Column(Integer, primary_key=True, index=True)
    mini_bar_stock = Column(Boolean, default=False)
    cleaned = Column(Boolean, default=False)

class ReservationModel(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String, index=True)
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    room_number = Column(Integer, index=True)

Base.metadata.create_all(bind=engine)

# Pydantic models for validation
class Room(BaseModel):
    room_number: int
    mini_bar_stock: bool = False
    cleaned: bool = False

    @validator('room_number')
    def room_number_positive(cls, v):
        if v <= 0:
            raise ValueError('Room number must be positive')
        return v

class Reservation(BaseModel):
    guest_name: str
    check_in_date: datetime
    check_out_date: datetime
    room_number: int

    @validator('room_number')
    def room_number_exists(cls, v):
        session = SessionLocal()
        room = session.query(RoomModel).filter(RoomModel.room_number == v).first()
        session.close()
        if not room:
            raise ValueError('Room number does not exist')
        return v

def manage_tasks():
    session = SessionLocal()
    
    # Check and refill mini-bars
    rooms = session.query(RoomModel).all()
    for room in rooms:
        if not room.mini_bar_stock:
            room.mini_bar_stock = True
            logger.info(f"Mini-bar in room {room.room_number} has been refilled.")
    
    # Clean rooms
    for room in rooms:
        if not room.cleaned:
            room.cleaned = True
            logger.info(f"Room {room.room_number} has been cleaned.")
    
    # Check reservations
    today = datetime.now().date()
    reservations = session.query(ReservationModel).filter(ReservationModel.check_in_date <= today,
                                                          ReservationModel.check_out_date >= today).all()
    for reservation in reservations:
        logger.info(f"Reservation for {reservation.guest_name} in room {reservation.room_number} is active.")
        send_email_notification(reservation.guest_name, reservation.room_number)
    
    session.commit()
    session.close()

def send_email_notification(guest_name, room_number):
    # Simulate sending an email (no actual sending for simplicity)
    logger.info(f"Email sent to {guest_name} regarding room {room_number} reservation.")

# Schedule tasks to run periodically
schedule.every().day.at("01:00").do(manage_tasks)  # Run tasks daily at 1 AM

# Main loop to keep the scheduler running
if __name__ == "__main__":
    logger.info("Hotel Management System started.")
    schedule.run_pending()