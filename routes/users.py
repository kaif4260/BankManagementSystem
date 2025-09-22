from fastapi import APIRouter, Depends, Request, HTTPException, security
from fastapi.security import HTTPAuthorizationCredentials
from models.users import ResponseSchema, TokenResponse, Register, Login, TokenResponse
from sqlalchemy.orm import Session, relationship
from config import get_db
from passlib.context import CryptContext
from repository.users import UserRepo, JWTRepo
from tables.users import Users, RefreshToken   # Define Refresh Token in this code block
from datetime import datetime, timedelta



router = APIRouter(
    tags={"Authentication"}
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto") 

#Register
 
@router.post("/signup")
async def signup(request: Register, db: Session = Depends(get_db)):
    try:
        
        #Insert Data
        _user = Users(
            username = request.username,
            password = pwd_context.hash(request.password),
            email = request.email,
            phone_number = request.phone_number,
            first_name = request.first_name,
            last_name = request.last_name
        )
        UserRepo.insert(db, _user)
        return ResponseSchema(code="200" or "201", status = "Done", message="Successfully Registered").model_dump(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(code="404", status="Error", message="Internal Server Error").model_dump(exclude_none=True)
    

#Login

@router.post("/login")
async def login(request: Login, db: Session = Depends (get_db)):

    try:
        # find user by username
        _user = UserRepo.find_by_username(db, Users, request.username)

        if not pwd_context.verify(request.password, _user.password):
            return ResponseSchema (code="404", status="Bad Request", messages="Invalid Password").model_dump(exclude_none=True)
        
        # Update Lost Login
        _user.last_login = datetime.utcnow()
        db.commit()


        access_token = JWTRepo.generate_token({"sub": _user.username}, expires_delta=timedelta(minutes=15))
        refresh_token = JWTRepo.generate_token({"sub": _user.username}, expires_delta=timedelta(days=7))

        print("Saving refresh token", refresh_token, "for user", _user.id)
        db.add(RefreshToken(user_id=_user.id, token = refresh_token))
        db.commit()
        saved = db.query(RefreshToken).filter_by(user_id=_user.id).all()
        print("Currently in DB:", len(saved), [r.token for r in saved])

        print("Saved token with ID", RefreshToken.id)

        # token = JWTRepo.generate token({'sub': _user.username})
        return ResponseSchema(code="200", status="Done", message = "Successfully Login", result =TokenResponse(access_token = access_token, refresh_token=refresh_token, token_type="bearer")).dict(exclude_none=True)
    
    
    except Exception as error:
        error_message = str(error.args)
        print(error_message)
        return ResponseSchema(code="500", status="Error", messages="Internal server error").model_dump(exclude_none=True)
    

@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    db_token = db.query(RefreshToken).filter_by(token= refresh_token).first()
    if not db_token or db_token.is_revoked:
        raise HTTPException(401, "Invalid refresh token")

    payload = JWTRepo.decode_token (refresh_token)
    if not payload:
        raise HTTPException(401, "Expired or bad token")

    new_access = JWTRepo.generate_token({"sub": payload["sub"]}, expires_delta = timedelta(minutes=15))
    return {"access_token": new_access, "token_type": "bearer"}
        

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    db_token = db.query(RefreshToken).filter_by(token = refresh_token).first()
    if db_token:
        db_token.is_revoked = True
        # Update Logout_time for the user
        _user = db.query(Users).filter(Users.id == db_token.user_id).first()
        if _user:
            _user.logout_time = datetime.utcnow()
        db.commit()    

    return {"message": "Logout Successfully"}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    payload = JWTRepo.decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(401, "Invalid access token")
    return payload["sub"]