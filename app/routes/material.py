from fastapi import APIRouter, Body, Depends, HTTPException, status,Query
from typing import Annotated
from ..db import SessionDep
from ..models.material import Material, MaterialIn, MaterialOut, MaterialService, MaterialUpdate
from .user import get_current_active_user
from ..models.user import UserOut
from datetime import date

materialRouter = APIRouter(tags=["Material"], prefix="/api")

@materialRouter.post("/material", status_code=status.HTTP_201_CREATED)
async def create_material(material: Annotated[MaterialIn, Body()], current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep) -> MaterialOut:
    try:
        return MaterialService.create_material(material, current_user.id, session)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating material")
    
@materialRouter.get("/material", response_model=list[MaterialOut], status_code=status.HTTP_200_OK)
async def get_materials(current_user:Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep, skip:int = 0, limit:int = 100) -> list[MaterialOut]:
    try:
        return MaterialService.get_materials(current_user.id, session, skip, limit)
    except Exception as e:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching materials")
@materialRouter.get("/material/{material_id}",response_model=MaterialOut, status_code=status.HTTP_200_OK)
async def get_material_by_id(material_id: int, current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep) -> MaterialOut:
    try:
        return MaterialService.get_material_by_id(material_id, current_user.id, session)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching material")
@materialRouter.delete("/material/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material(material_id: int, current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep):
    try:
        MaterialService.delete_material(material_id, current_user.id, session)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting material")    

@materialRouter.patch("/material/{material_id}", status_code=status.HTTP_200_OK)
async def update_material(material_id:int, material_update: Annotated[MaterialUpdate, Body()],current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep) -> MaterialOut:
    try:
        return MaterialService.update_material(material_id, material_update, current_user.id, session)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating material")
    
@materialRouter.put("/material/{material_id}", status_code=status.HTTP_200_OK)
async def replace_material(material_id:int, material: Annotated[MaterialIn, Body()], current_user: Annotated[UserOut, Depends(get_current_active_user)], session: SessionDep) -> MaterialOut:
    try:

        return MaterialService.replace_material(material_id, material, current_user.id, session)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error replacing material")