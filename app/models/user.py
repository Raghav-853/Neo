from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base
import enum

class UserRole(str, enum.Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.viewer, nullable=False)
