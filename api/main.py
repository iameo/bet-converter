from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from fastapi.middleware.cors import CORSMiddleware

from .views.matches_view import match_view
from .views.slips_view import slip_view

app = FastAPI(
    title="BET CONVERTER",
    description="API for converting a bet slip from one source to another!",
    version="alpha")



origins = [
    "http://127.0.0.1:5000",
        "http://127.0.0.1:8080",
    # "https://localhost",
    # "http://localhost",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Redirect to docs
@app.get("/", tags=['Docs'])
def docs():
    return RedirectResponse('/docs')

app.include_router(match_view,prefix="/api/v1/resources",tags=["Matches"])
app.include_router(slip_view,prefix="/api/v1/resources",tags=["Slips"])
