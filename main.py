from fastapi import FastAPI, status, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
import schemas
from database import get_db
from routers import user_router, abbr_router
from services import slang_service
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from datetime import timedelta
import time


app = FastAPI(
    title="Slangs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def log_middleware(request: Request, call_next):
    start_time = time.time()
     # Call the next middleware or route handler
    response = call_next(request)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Request: {request.method} {request.url} | Duration: {duration:.4f} seconds")
    return response


app.middleware("http")(log_middleware)


app.include_router(user_router.router)
app.include_router(abbr_router.router)


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/submit", response_class=HTMLResponse)
async def submit(request: Request):
    return templates.TemplateResponse("submit.html", {"request": request})


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/slangs/{filename}", status_code=status.HTTP_201_CREATED)
def read_and_insert_slangs(
    filename: str, 
    db: Session = Depends(get_db)
):
    return slang_service.read_and_insert_slangs(filename=filename, db=db)