from fastapi import APIRouter, Body, Depends, HTTPException, status,Query
from typing import Annotated
from ..db import SessionDep
from ..models.event import EventIn, EventOut, EventUpdate, EventService
from .user import get_current_active_user
from ..models.user import UserOut
from datetime import date
from ..exceptions import EventNotFoundException

eventRouter = APIRouter(tags=["Event"], prefix="/api")


@eventRouter.post("/event", status_code=status.HTTP_201_CREATED, response_model=EventOut)
async def create_event(event: Annotated[EventIn, Body()], current_user: Annotated[UserOut, Depends(get_current_active_user)],session: SessionDep)->EventOut:
    try:
        eventDB = EventService.create_event(event, session, current_user.email)
        return eventDB
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating event")
@eventRouter.get("/event", response_model=list[EventOut], status_code=status.HTTP_200_OK)
async def get_events(current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep,fromDate: Annotated[date | None, Query(description="Filter events from specific date")]=None,toDate: Annotated[date | None, Query(description="Filter events to specific date")]=None,skip:int = 0, limit:int = 100) -> list[EventOut]:
    try:
        events = EventService.getEvents(session,fromDate,toDate,skip, limit)
        return events
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching events")
@eventRouter.get("/event/{event_id}", response_model=EventOut, status_code=status.HTTP_200_OK)
async def get_event_by_id(event_id:int, current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep) -> EventOut:
    try:
        event = EventService.getEventById(event_id, session)
        return event
    except EventNotFoundException as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching event")
@eventRouter.delete("/event/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteEvent(event_id:int, current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep):
    try:
        EventService.deleteEvent(event_id, session)
    except EventNotFoundException as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting event")

@eventRouter.patch("/event/{event_id}",status_code=status.HTTP_200_OK, response_model=EventOut)
async def updateEvent(event_id:int,event_update: Annotated[EventUpdate,Body()],current_user: Annotated[UserOut, Depends(get_current_active_user)],session: SessionDep) -> EventOut:
    try:
        event = EventService.updateEvent(event_id, event_update, session)
        return event
    except EventNotFoundException as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating event")
@eventRouter.put("/event/{event_id}",status_code=status.HTTP_200_OK, response_model=EventOut)
async def replaceEvent(event_id:int,event_update: Annotated[EventIn,Body()],current_user: Annotated[UserOut, Depends(get_current_active_user)],session: SessionDep) -> EventOut:
    try:
        event = EventService.replaceEvent(event_id, event_update, session)
        return event
    except EventNotFoundException as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error updating event')