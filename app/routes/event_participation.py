from fastapi import APIRouter, Body, Depends, HTTPException, status
from typing import Annotated
from ..db import SessionDep
from ..models.event_participation import Participate, ParticipationService
from .user import get_current_active_user
from ..models.user import UserOut
from ..exceptions import EventNotFoundException, UserAlreadyParticipatingException, UserParticipationNotFoundException

participationRouter = APIRouter(tags=["Event Participation"], prefix="/api")

@participationRouter.post("/participate/{event_id}", status_code=status.HTTP_201_CREATED, response_model=Participate)
async def add_event_participation(event_id: int, current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep) -> Participate:
    try:
        return ParticipationService.add_event_participation(event_id, current_user.id, session)
    except EventNotFoundException as enf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(enf))
    except UserAlreadyParticipatingException as uap:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(uap))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error adding event participation")

@participationRouter.get("/participations", response_model=list[Participate], status_code=status.HTTP_200_OK)
async def get_participations_by_user(current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep) -> list[Participate]:
    try:
        return ParticipationService.get_participations_by_user(current_user.id, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching participations")

@participationRouter.delete("/participate/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_participation(event_id: int, current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep):
    try:
        ParticipationService.delete_event_participation(event_id, current_user.id, session)
    except UserParticipationNotFoundException as upnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(upnf))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting event participation")    