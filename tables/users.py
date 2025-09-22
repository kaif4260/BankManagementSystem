from sqlalchemy import Integer, String, Boolean, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship
from config import Base
import datetime

class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(150))
    email = Column(String(200))
    phone_number = Column(String(20))
    first_name = Column(String(50))
    last_name = Column(String(50))

    last_login = Column(DateTime, default=None)
    logout_time = Column(DateTime, default=None)

    #Device Info = Column(String(100))

    device_info = Column(String(100))
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, default=None, onupdate = datetime.datetime.utcnow)

    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        primaryjoin = "Users.id == RefreshToken.user_id"
    )

    #token = Column(string(500), unique =True, index = True)
    #created_at = Column (DateTime, default datetime.datetime.utcnow)
    #is_revoked = Column(Boolean, default=False)

class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(512), unique = True, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default = datetime.datetime.utcnow())

    user = relationship("Users", back_populates="refresh_tokens")