from fastapi import FastAPI
from app.database import Base, engine
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.routers.visitor_router import router as visitor_router
from app.routers.visit_router import router as visit_router

app = FastAPI(
    title="Visitor Management System",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(visitor_router)
app.include_router(visit_router)


@app.get("/")
def home():
    return {
        "message": "Visitor Management System API"
    }