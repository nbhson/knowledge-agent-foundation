from typing import Dict, List, Optional


class CodeGenerator:
    """
    Tự động generate code từ templates và specifications.
    
    Supports:
    - CRUD from database schema
    - API endpoints from OpenAPI spec
    - Tests from source code
    - Documentation from code comments
    """
    
    def __init__(self, template_dir: str = "./templates"):
        self.template_dir = template_dir
        self.templates: Dict[str, str] = {}
    
    def generate_crud(self, model_name: str, 
                      fields: Dict[str, str],
                      output_dir: str = "./generated") -> List[str]:
        """
        Generate CRUD operations từ model definition.
        
        Args:
            model_name: Name of the model (e.g., "User")
            fields: Dict of field_name -> field_type
            output_dir: Where to write generated files
            
        Returns:
            List of generated file paths
        """
        generated_files = []
        
        # Generate model
        model_code = self._generate_model(model_name, fields)
        model_path = f"{output_dir}/models/{model_name.lower()}.py"
        generated_files.append(model_path)
        
        # Generate schema
        schema_code = self._generate_schema(model_name, fields)
        schema_path = f"{output_dir}/schemas/{model_name.lower()}.py"
        generated_files.append(schema_path)
        
        # Generate service
        service_code = self._generate_service(model_name, fields)
        service_path = f"{output_dir}/services/{model_name.lower()}.py"
        generated_files.append(service_path)
        
        # Generate API routes
        route_code = self._generate_routes(model_name, fields)
        route_path = f"{output_dir}/routes/{model_name.lower()}.py"
        generated_files.append(route_path)
        
        # Generate tests
        test_code = self._generate_tests(model_name, fields)
        test_path = f"{output_dir}/tests/test_{model_name.lower()}.py"
        generated_files.append(test_path)
        
        return generated_files
    
    def _generate_model(self, name: str, 
                       fields: Dict[str, str]) -> str:
        """Generate SQLAlchemy model"""
        type_map = {
            "str": "String(255)",
            "int": "Integer",
            "float": "Float",
            "bool": "Boolean",
            "datetime": "DateTime",
            "text": "Text",
        }
        
        fields_code = []
        for fname, ftype in fields.items():
            sql_type = type_map.get(ftype, "String(255)")
            fields_code.append(
                f"    {fname} = Column({sql_type}, nullable=False)"
            )
        
        return f'''
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.database import Base


class {name}(Base):
    __tablename__ = "{name.lower()}s"
    
    id = Column(Integer, primary_key=True, index=True)
{chr(10).join(fields_code)}
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
'''
    
    def _generate_schema(self, name: str, 
                        fields: Dict[str, str]) -> str:
        """Generate Pydantic schema"""
        type_map = {
            "str": "str",
            "int": "int",
            "float": "float",
            "bool": "bool",
            "datetime": "datetime",
            "text": "str",
        }
        
        fields_code = []
        for fname, ftype in fields.items():
            py_type = type_map.get(ftype, "str")
            fields_code.append(f"    {fname}: {py_type}")
        
        return f'''
from pydantic import BaseModel
from datetime import datetime


class {name}Base(BaseModel):
{chr(10).join(fields_code)}


class {name}Create({name}Base):
    pass


class {name}Update(BaseModel):
{chr(10).join([f"    {f}: Optional[{type_map.get(t, 'str')}] = None" for f, t in fields.items()])}


class {name}Response({name}Base):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
'''
    
    def _generate_service(self, name: str, 
                         fields: Dict[str, str]) -> str:
        """Generate service layer"""
        return f'''
from typing import List, Optional
from app.models.{name.lower()} import {name}
from app.schemas.{name.lower()} import {name}Create, {name}Update
from sqlalchemy.orm import Session


class {name}Service:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[{name}]:
        return db.query({name}).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[{name}]:
        return db.query({name}).filter({name}.id == id).first()
    
    @staticmethod
    def create(db: Session, data: {name}Create) -> {name}:
        obj = {name}(**data.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    @staticmethod
    def update(db: Session, id: int, data: {name}Update) -> Optional[{name}]:
        obj = db.query({name}).filter({name}.id == id).first()
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj
    
    @staticmethod
    def delete(db: Session, id: int) -> bool:
        obj = db.query({name}).filter({name}.id == id).first()
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True
'''
    
    def _generate_routes(self, name: str, 
                        fields: Dict[str, str]) -> str:
        """Generate FastAPI routes"""
        return f'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.{name.lower()} import {name}Create, {name}Update, {name}Response
from app.services.{name.lower()} import {name}Service

router = APIRouter(prefix="/{name.lower()}s", tags=["{name.lower()}s"])


@router.get("/", response_model=List[{name}Response])
def list_{name.lower()}s(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return {name}Service.get_all(db, skip, limit)


@router.get("/{{id}}", response_model={name}Response)
def get_{name.lower()}(id: int, db: Session = Depends(get_db)):
    obj = {name}Service.get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="{name} not found")
    return obj


@router.post("/", response_model={name}Response, status_code=201)
def create_{name.lower()}(data: {name}Create, db: Session = Depends(get_db)):
    return {name}Service.create(db, data)


@router.patch("/{{id}}", response_model={name}Response)
def update_{name.lower()}(id: int, data: {name}Update, db: Session = Depends(get_db)):
    obj = {name}Service.update(db, id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="{name} not found")
    return obj


@router.delete("/{{id}}", status_code=204)
def delete_{name.lower()}(id: int, db: Session = Depends(get_db)):
    if not {name}Service.delete(db, id):
        raise HTTPException(status_code=404, detail="{name} not found")
'''
    
    def _generate_tests(self, name: str, 
                       fields: Dict[str, str]) -> str:
        """Generate pytest tests"""
        sample_data = ", ".join([
            f'"{f}": "test_{f}"' if t == "str" else f'"{f}": 1'
            for f, t in fields.items()
        ])
        
        return f'''
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class Test{name}CRUD:
    def test_create_{name.lower()}(self):
        response = client.post("/{name.lower()}s/", json={{{sample_data}}})
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
    
    def test_get_{name.lower()}(self):
        # Create first
        create_resp = client.post("/{name.lower()}s/", json={{{sample_data}}})
        id = create_resp.json()["id"]
        
        response = client.get(f"/{name.lower()}s/{{id}}")
        assert response.status_code == 200
    
    def test_list_{name.lower()}s(self):
        response = client.get("/{name.lower()}s/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_delete_{name.lower()}(self):
        create_resp = client.post("/{name.lower()}s/", json={{{sample_data}}})
        id = create_resp.json()["id"]
        
        response = client.delete(f"/{name.lower()}s/{{id}}")
        assert response.status_code == 204
'''
