from pydantic import BaseModel, Field
from datetime import date as dt_date, datetime, timezone
from sqlmodel import SQLModel, Field as sqlmodel_Field, Session, select
from ..exceptions import EventNotFoundException

class EventIn(BaseModel):
    name: str  = Field(description="Name of the event",min_length=10,max_length=50)
    description: str = Field(description="Description of the event", min_length=10, max_length=255)
    date: dt_date = Field(description="Date of the event")
    city: str = Field(description="City of the event", min_length=5, max_length=50)
    street: str | None = Field(description="Street of the event", max_length=100, default=None)
    number: int | None = Field(description="Number of street", default=None)
    zipCode: int | None = Field(description="Zip code of the city", default=None)
    autoOrganized: bool | None = Field(description="Indicates if the event is auto-organized", default=None)

class EventOut(EventIn):
    eventId: int = Field(description="Unique identifier of the event")

class EventUpdate(BaseModel):
    name: str | None = Field(default=None,description="Name of the event",min_length=10,max_length=50)
    description: str | None = Field(default=None,description="Description of the event", min_length=10, max_length=255)
    date: dt_date | None = Field(description="Date of the event", default=None)
    city: str | None = Field(description="City of the event", min_length=5, max_length=50, default=None)
    street: str | None = Field(description="Street of the event", max_length=100, default=None)
    number: int | None = Field(description="Number of street", default=None)
    zipCode: int | None = Field(description="Zip code of the city", default=None)
    autoOrganized: bool | None = Field(description="Indicates if the event is auto-organized", default=None)

class Event(SQLModel, table=True):
    eventId: int | None = sqlmodel_Field(default=None, primary_key=True)
    name: str = sqlmodel_Field(min_length=10, max_length=50)
    description: str = sqlmodel_Field(min_length=10, max_length=255)
    date: dt_date
    city: str = sqlmodel_Field(min_length=5, max_length=50)
    street: str | None = sqlmodel_Field(default=None, min_length=0, max_length=100)
    number: int | None = sqlmodel_Field(default=None)
    zipCode: int | None = sqlmodel_Field(default=None)
    autoOrganized: bool | None = sqlmodel_Field(default=None)
    active: bool = sqlmodel_Field(default=True)
    creationDate: datetime = sqlmodel_Field(default_factory=lambda: datetime.now(timezone.utc))
    lastModifiedDate: datetime = sqlmodel_Field(default_factory=lambda: datetime.now(timezone.utc))
    createdBy: str | None = sqlmodel_Field(default=None)

class EventService:
    @staticmethod
    def create_event(event_in: EventIn, session: Session, user_email) -> Event:
        try:
            eventDB = Event(
                name=event_in.name,
                description=event_in.description,
                date = event_in.date,
                city=event_in.city,
                street=event_in.street,
                number=event_in.number,
                zipCode=event_in.zipCode,
                autoOrganized=event_in.autoOrganized,
                creationDate=datetime.now(timezone.utc),
                lastModifiedDate=datetime.now(timezone.utc),
                createdBy=user_email
            )
            session.add(eventDB)
            session.commit()
            session.refresh(eventDB)
            return eventDB
        except Exception as e:
            raise Exception(f"Error creating event: {str(e)}")
    @staticmethod
    def getEvents(session: Session, fromDate: dt_date, toDate:dt_date,skip:int, limit:int) -> list[Event]:
        try:
            if not fromDate and not toDate:
                statement = select(Event).offset(skip).limit(limit).where(Event.active == True)
            elif fromDate and not toDate:
                statement = select(Event).where(Event.date >= fromDate, Event.active == True).offset(skip).limit(limit)    
            elif not fromDate and toDate:   
                statement = select(Event).where(Event.date <= toDate, Event.active == True).offset(skip).limit(limit)    
            else:
                statement = select(Event).where(Event.date >= fromDate, Event.date <= toDate, Event.active == True).offset(skip).limit(limit)
            events = session.exec(statement)
            return events
        except Exception as e:
            raise Exception(f"Error fetching events: {str(e)}")
    @staticmethod
    def getEventById(id:int, session: Session) -> Event:
        statement = select(Event).where(Event.eventId == id, Event.active == True)
        try:
            event= session.exec(statement).first()
        except Exception as e:
            raise Exception(f"Error fetching event: {str(e)}")      
        if event:
            return event
        else:
            raise EventNotFoundException(f"Event with id {id} not found o inactive")
    
    @staticmethod
    def deleteEvent(id:int, session: Session):
        statement = select(Event).where(Event.eventId == id, Event.active == True)
        try:
            event= session.exec(statement).first()
        except Exception as e:
            raise Exception(f"Error deleting event: {str(e)}")   
        if event and event.active:
            event.active = False
            event.lastModifiedDate = datetime.now(timezone.utc)
            session.add(event)
            session.commit()
        else: 
            raise EventNotFoundException(f"Event with id {id} not found o inactive")
    @staticmethod
    def updateEvent(id:int,event_update:EventUpdate,session: Session) -> Event:
        statement = select(Event).where(Event.eventId == id, Event.active == True)
        try:
            eventDb= session.exec(statement).first()
        except Exception as e:
            raise Exception(f"Error updating event: {str(e)}")
        if eventDb:
            update_data = event_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(eventDb, key, value)
            eventDb.lastModifiedDate = datetime.now(timezone.utc)
            session.add(eventDb)
            session.commit()
            session.refresh(eventDb)    
            return eventDb
        else:
            raise EventNotFoundException(f"Event with id {id} not found o inactive")
    @staticmethod
    def replaceEvent(id:int, event_replace:EventIn, session: Session) -> Event:
        statement = select(Event).where(Event.eventId == id, Event.active == True)
        try:
            eventDb= session.exec(statement).first()
        except Exception as e:
            raise Exception(f"Error updating event: {str(e)}")
        if eventDb:
            eventDb.name = event_replace.name
            eventDb.description = event_replace.description
            eventDb.date = event_replace.date
            eventDb.city = event_replace.city 
            eventDb.street = event_replace.street 
            eventDb.number = event_replace.number 
            eventDb.zipCode = event_replace.zipCode 
            eventDb.autoOrganized = event_replace.autoOrganized
            eventDb.lastModifiedDate = datetime.now(timezone.utc)
            session.add(eventDb)
            session.commit()
            session.refresh(eventDb)    
            return eventDb
        else:
            raise EventNotFoundException(f"Event with id {id} not found o inactive")
        

