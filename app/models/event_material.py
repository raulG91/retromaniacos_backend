from pydantic import BaseModel, Field
from datetime import date, datetime, timezone
from sqlmodel import SQLModel, Field as sqlmodel_Field, Session, select
from .material import Material
from .event import Event
from ..exceptions import EventNotFoundException,MaterialNotFoundException,MaterialAlreadyAssociatedException,EventMaterialNotFoundException

class EventMaterial(SQLModel, table=True):
    materialId: int = sqlmodel_Field(default=None, primary_key=True, foreign_key="material.materialId")
    eventId: int = sqlmodel_Field(default=None, primary_key=True, foreign_key="event.eventId")
    active: bool = sqlmodel_Field(default=True)
    modifyBy : int = sqlmodel_Field(default=None)
    creationDate: datetime = sqlmodel_Field(default_factory=lambda: datetime.now(timezone.utc))
    lastModifiedDate: datetime = sqlmodel_Field(default_factory=lambda: datetime.now(timezone.utc))


class EventMaterialService:
    @staticmethod
    def add_material_event(eventId: int, materialId: int, user_id:int, session:Session) -> EventMaterial:
        try:
            statment = select(Event).where(Event.eventId == eventId,Event.active == True)
            eventDB = session.exec(statment).first()
        except Exception as e:
            raise Exception(f"Error adding material to event: {str(e)}")    
        if  eventDB is None:
            raise EventNotFoundException("Event not found")
        #Check if material exist and its active
        try: 
            statement = select(Material).where(Material.materialId == materialId, Material.active == True)
            materialDB = session.exec(statement).first()
        except Exception as e:
            raise Exception(f"Error adding material to event: {str(e)}")    
        if materialDB is None:
            raise MaterialNotFoundException("Material not found or inactive")
        #Check if the material is already associated with the event
        try:
            statement = select(EventMaterial).where(EventMaterial.eventId == eventId, EventMaterial.materialId == materialId, EventMaterial.active == True)
            event_materialDB = session.exec(statement).first()
        except Exception as e:
            raise Exception(f"Error retrieving event material: {str(e)}")    
        if event_materialDB is not None:
            raise MaterialAlreadyAssociatedException("Material is already associated with the event")
        
        EventMaterialDB = EventMaterial(eventId=eventId, materialId=materialId, active=True, modifyBy=user_id)
        try: 
            session.add(EventMaterialDB)
            session.commit()
            session.refresh(EventMaterialDB)
            return EventMaterialDB
        except Exception as e:
            session.rollback()
            raise Exception(f"Error adding material to event: {str(e)}")
        
    @staticmethod
    def get_materials_by_event(eventId: int, user_id:int, session:Session) -> list[EventMaterial]:
        try:
            statment = select(Event).where(Event.eventId == eventId,Event.active == True)
            eventDB = session.exec(statment).first()
        except Exception as e:
            raise Exception(f"Error retrieving materials for event: {str(e)}")    
        if  eventDB is None:
            raise EventNotFoundException("Event not found")
        try:
            statement = select(EventMaterial).where(EventMaterial.eventId == eventId, EventMaterial.active == True)
            event_materialsDB = session.exec(statement).all()
            return event_materialsDB
        except Exception as e:
            raise Exception(f"Error retrieving materials for event: {str(e)}")
    @staticmethod
    def remove_material_event(eventId: int, materialId: int,userId, session: Session)->None:

        #First action is to check if the event exists
        try: 
            statement = select(Event).where(Event.eventId == eventId, Event.active == True)
            eventDB = session.exec(statement).first()
        except Exception as e:
            raise Exception(f"Error retriving event: {str(e)}")    
        if eventDB is None:
            raise EventNotFoundException("Event not found")
        #Check if material exists and is active
        try: 
            statement = select(Material).where(Material.materialId == materialId, Material.active == True)
            materialDB = session.exec(statement).first()
        except Exception as e:
            raise Exception(f"Error retriving material: {str(e)}")
        if materialDB is None:
            raise MaterialNotFoundException("Material not found or inactive")
        #Check if the material is associated with the event
        try:
            statement = select(EventMaterial).where(EventMaterial.eventId == eventId, EventMaterial.materialId == materialId, EventMaterial.active == True)
            event_materialDB = session.exec(statement).first()
        except Exception as e:
            raise Exception(f"Error retriving event material: {str(e)}")
        
        if event_materialDB is None:
            raise EventMaterialNotFoundException("Material is not associated with the event") 
        else:
            #if material is associated with the event, we will set the active field to False
            try:
                event_materialDB.active = False
                event_materialDB.lastModifiedDate = datetime.now(timezone.utc)
                event_materialDB.modifyBy = userId
                session.add(event_materialDB)
                session.commit()
            except Exception as e:
                session.rollback()
                raise Exception(f"Error removing material from event: {str(e)}")