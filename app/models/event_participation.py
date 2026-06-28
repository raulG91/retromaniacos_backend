from pydantic import BaseModel, Field
from datetime import date, datetime, timezone
from sqlmodel import SQLModel, Field as sqlmodel_Field, Session, select
from .event import Event
from ..exceptions import EventNotFoundException, UserAlreadyParticipatingException,UserParticipationNotFoundException
class Participate(SQLModel, table=True):
    eventId: int | None = sqlmodel_Field(default=None, primary_key=True, foreign_key="event.eventId")
    userId: int | None = sqlmodel_Field(default=None, primary_key=True, foreign_key="user.id")
    active: bool = sqlmodel_Field(default=True)
    creationDate: datetime = sqlmodel_Field(default_factory=lambda: datetime.now(timezone.utc))
    lastModifiedDate: datetime = sqlmodel_Field(default_factory=lambda: datetime.now(timezone.utc))

class ParticipationService:
    @staticmethod
    def add_event_participation(event_id: int, user_id: int, session: Session) -> Participate:
        try:
            statment = select(Event).where(Event.eventId == event_id,Event.active == True)
            eventDB = session.exec(statment).first()
        except Exception as e:
            session.rollback()
            raise Exception(f"Error adding event participation: {str(e)}")    
        if  eventDB is None:
            raise EventNotFoundException("Event not found")
        #Check if the user is already participating in the event
        try:
            statement = select(Participate).where(Participate.eventId == event_id, Participate.userId == user_id, Participate.active == True)
            participationDB = session.exec(statement).first()
        except Exception as e:
            session.rollback()
            raise Exception(f"Error retrieving event participation: {str(e)}")    
        if participationDB is not None: #User is already participating in the event
            raise UserAlreadyParticipatingException("User is already participating in the event")
        #Check if user participation record exists but is inactive, if so, reactivate it
        try:
            statement = select(Participate).where(Participate.eventId == event_id, Participate.userId == user_id, Participate.active == False)
            inactive_participationDB = session.exec(statement).first()
        except Exception as e:
            session.rollback()
            raise Exception(f"Error retrieving event participation: {str(e)}")
        if inactive_participationDB is not None:
            inactive_participationDB.active = True
            inactive_participationDB.lastModifiedDate = datetime.now(timezone.utc)
            try:
                session.add(inactive_participationDB)
                session.commit()
                session.refresh(inactive_participationDB)
                return inactive_participationDB
            except Exception as e:
                session.rollback()
                raise Exception(f"Error reactivating event participation: {str(e)}")
        participation = Participate(eventId=event_id, userId=user_id, active= True)      
        try:
            session.add(participation)
            session.commit()
            session.refresh(participation)
            return participation
        except Exception as e:
            session.rollback()
            raise Exception(f"Error adding event participation: {str(e)}")
    @staticmethod
    def get_participations_by_user(user_id: int, session: Session) -> list[Participate]:
        try:
            statement = select(Participate).where(Participate.userId == user_id, Participate.active == True)
            participations = session.exec(statement)
            return participations
        except Exception as e:
            raise Exception(f"Error fetching participations: {str(e)}")    
    @staticmethod
    def delete_event_participation(event_id: int, user_id: int, session: Session):
        try:
            statement = select(Participate).where(Participate.eventId == event_id, Participate.userId == user_id, Participate.active == True)
            participationDB = session.exec(statement).first()
        except Exception as e:
            session.rollback()
            raise Exception(f"Error retrieving event participation: {str(e)}")    
        if participationDB is None:
            raise UserParticipationNotFoundException("User is not participating in the event")
        try:
            participationDB.active = False
            participationDB.lastModifiedDate = datetime.now(timezone.utc)
            session.add(participationDB)
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"Error deleting event participation: {str(e)}")