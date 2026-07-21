from fastapi import APIRouter, Body, Depends, HTTPException, status
from typing import Annotated
from ..db import SessionDep
from ..models.event_material import EventMaterial, EventMaterialService
from .user import get_current_active_user
from ..models.user import UserOut
from ..exceptions import EventNotFoundException,MaterialNotFoundException,MaterialAlreadyAssociatedException,EventMaterialNotFoundException

eventMaterialRouter = APIRouter(tags=["Event Material"], prefix="/api")

@eventMaterialRouter.post("/event/{event_id}/material/{material_id}", status_code=status.HTTP_201_CREATED, response_model=EventMaterial)
async def add_meterial_to_event(event_id: int, material_id: int, current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep) -> EventMaterial:
    try:
        return EventMaterialService.add_material_event(event_id, material_id, current_user.id, session)
    except EventNotFoundException as enf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(enf))
    except MaterialNotFoundException as mnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(mnf))
    except MaterialAlreadyAssociatedException as maae:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(maae))
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error adding material to event")

@eventMaterialRouter.get("/event/{event_id}/material", status_code=status.HTTP_200_OK, response_model=list[EventMaterial],description="Get all materials associated with an event")
async def get_materials_by_event(event_id: int, current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep) -> list[EventMaterial]:
    try:
        return EventMaterialService.get_materials_by_event(event_id, current_user.id, session)
    except EventNotFoundException as enf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(enf))
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving materials for event")

@eventMaterialRouter.delete("/event/{event_id}/material/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_material_from_event(event_id: int, material_id: int, current_user: Annotated[UserOut, Depends(get_current_active_user)],session: SessionDep) -> None:
    try:
        EventMaterialService.remove_material_event(event_id, material_id, current_user.id, session)
    except EventNotFoundException as enf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(enf))
    except MaterialNotFoundException as mnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(mnf))
    except EventMaterialNotFoundException as emnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(emnf))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error removing material from event") 