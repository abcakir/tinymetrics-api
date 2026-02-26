from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    click_count = Column(Integer, default=0)

    # Verknüpfung zum User (Foreign Key)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Zeitstempel
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Beziehung
    owner = relationship("User", backref="urls")