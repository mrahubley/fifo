from fastapi import FastAPI
from .routers import accounts, jobs, profiles, countries, degrees, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)
app.include_router(accounts.router)
app.include_router(profiles.router)
app.include_router(countries.router)
app.include_router(degrees.router)
app.include_router(auth.router)



@app.get('/')
def home():
    return { 'Home' }

