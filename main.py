from fastapi import FastAPI
from config import engine
from tables.users import Base


import tables.users as user_tables
import routes.users as user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include user-related routes
app.include_router(user_routes.router, tags=["Users"])
# app.include_router(user_routes.router)