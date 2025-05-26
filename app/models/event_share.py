from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.user import UserRole

class EventShare(Base):
    __tablename__ = "event_shares"
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(Enum(UserRole), nullable=False)

    event = relationship("Event", backref="shared_with")
    user = relationship("User", backref="shared_events") 