from typing import Generic, Optional, TypeVar
from sqlalchemy.orm import Session

import datetime
from datetime import datetime, timedelta

from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM

from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials


T = TypeVar('T')

#Users

class BaseRepo():
    @staticmethod
    def insert(db: Session, model: Generic[T]):

        db.add(model)
        db.commit()
        db.refresh(model)

class UserRepo(BaseRepo):

    @staticmethod
    def find_by_username(db: Session, model: Generic[T], username: str): 
        return db.query(model).filter(model.username == username).first()

#Token

class JWTRepo():
    @staticmethod
    def generate_token(data: dict, expires_delta: Optional[timedelta]=None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
        return encode_jwt
    
    @staticmethod
    def decode_token(token: str):
        try:

            # = jwt.decode(token, SECRET KEY, algorithms = [ALGORITHM])
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp = payload.get("exp")
        
            if exp and datetime.utcnow().timestamp() < exp :
                return payload
            return None

            return decode_token if decode_token['expires'] >= datetime.time() else None
        except JWTError as e:
            #print("Token decode error:", str(e))
            return None
            return{}