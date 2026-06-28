from pydantic import BaseModel, Field
from enum import Enum
from datetime import date, datetime, timezone
from sqlmodel import SQLModel, Field as sqlmodel_Field, Session, select
from ..exceptions import MaterialNotFoundException
class MaterialType(str,Enum):
    CONSOLE = "Console"
    GAME = "Game"
    PC = "PC"
    TV = "TV"
    ACCESORY = "Accesory"
    OTHER = "Other"


class MaterialIn(BaseModel):
    name : str = Field(description="Name of the item", min_length=1, max_length=100)
    description : str = Field(description="Description of the item", min_length=10, max_length=500)
    type : MaterialType = Field(description="Type of the item")

class MaterialUpdate(BaseModel):
    name: str | None = Field(description="Name of the item", min_length=1, max_length=100, default=None)
    description: str | None = Field(description="Description of the item", min_length=10, max_length=500, default=None)
    type: MaterialType | None = Field(description="Type of the item", min_length=1, max_length=50, default=None)
class MaterialOut(MaterialIn):
    materialId: int = Field(description="Unique identifier for the material")

class Material(SQLModel, table=True):
    materialId: int | None = sqlmodel_Field(default=None, primary_key=True)
    ownerId: int | None = sqlmodel_Field(description="ID of the user who owns the material",foreign_key="user.id")
    name : str = sqlmodel_Field(description="Name of the item", min_length=1, max_length=100)
    description : str = sqlmodel_Field(description="Description of the item", min_length=10, max_length=500)
    type : str = sqlmodel_Field(description="Type of the item", min_length=1, max_length=50)
    createdBy: str | None = sqlmodel_Field(description="ID of the user who created the material")
    creationDate: datetime = sqlmodel_Field(default_factory=lambda: datetime.now(timezone.utc))
    lastModifiedDate: datetime = sqlmodel_Field(default_factory=lambda: datetime.now(timezone.utc))
    active : bool = sqlmodel_Field(default=True)


class MaterialService:
    @staticmethod
    def create_material(material: MaterialIn, current_user_id: int,session: Session) -> Material:
        try:
            materialDB = Material(
                name=material.name,
                ownerId=current_user_id,
                description=material.description,
                type=material.type,
                createdBy=current_user_id,
                creationDate=datetime.now(timezone.utc),
                lastModifiedDate=datetime.now(timezone.utc),
                active=True
            )
            session.add(materialDB)
            session.commit()
            session.refresh(materialDB)
            return materialDB
        except Exception as e:
            session.rollback()
            raise Exception(f"Error creating material: {str(e)}")
    @staticmethod
    def get_materials(userId:int,session: Session, skip: int = 0, limit: int = 100) -> list[Material]:
        try:
            statement = select(Material).where(Material.active == True,Material.ownerId == userId).offset(skip).limit(limit)
            results = session.exec(statement)
            return results
        except Exception as e:
            raise Exception(f"Error fetching materials: {str(e)}")
    @staticmethod
    def get_material_by_id(materialId: int, userId: int, session: Session) -> Material:
        try:
            statement = select(Material).where(Material.materialId == materialId, Material.ownerId == userId ,Material.active == True)
            material = session.exec(statement).first()
        except Exception as e:
            raise Exception(f"Error fetching material: {str(e)}")        
        if not material:
            raise MaterialNotFoundException("Material not found")
        return material
  
    @staticmethod
    def delete_material(materialId: int, userId: int, session: Session):
        try:
            statement = select(Material).where(Material.materialId == materialId, Material.ownerId == userId ,Material.active == True)
            material = session.exec(statement).first()
        except Exception as e:
                raise Exception(f"Error fetching material: {str(e)}")    
        if not material:
            raise MaterialNotFoundException("Material not found")
        material.active = False
        material.lastModifiedDate = datetime.now(timezone.utc)
        try:
            session.add(material)
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"Error deleting material: {str(e)}")
    @staticmethod
    def update_material(materialId: int, material_update: MaterialUpdate, userId: int, session: Session) -> Material:
        try:
            statement = select(Material).where(Material.materialId == materialId, Material.ownerId == userId ,Material.active == True)
            material = session.exec(statement).first()
        except Exception as e:
                raise Exception(f"Error fetching material: {str(e)}")    
        if not material:
            raise MaterialNotFoundException("Material not found")
        if material_update.name is not None:
            material.name = material_update.name
        if material_update.description is not None:
            material.description = material_update.description
        if material_update.type is not None:
            material.type = material_update.type
        material.lastModifiedDate = datetime.now(timezone.utc)
        try:
            session.add(material)
            session.commit()
            session.refresh(material)
            return material
        except Exception as e:
            session.rollback()
            raise Exception(f"Error updating material: {str(e)}")
    @staticmethod
    def replace_material(materialId:int, materialReplace: MaterialIn,userId, session: Session) -> Material:
        try:
            statement = select(Material).where(Material.materialId == materialId, Material.ownerId == userId ,Material.active == True)
            material = session.exec(statement).first()
        except Exception as e:
                raise Exception(f"Error fetching material: {str(e)}")    
        if not material:
            raise MaterialNotFoundException("Material not found")
        material.name = materialReplace.name
        material.description = materialReplace.description
        material.type = materialReplace.type
        material.lastModifiedDate = datetime.now(timezone.utc)
        try:
            session.add(material)
            session.commit()
            session.refresh(material)
            return material
        except Exception as e:
            session.rollback()
            raise Exception(f"Error replacing material: {str(e)}")