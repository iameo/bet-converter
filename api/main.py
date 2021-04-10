from fastapi import FastAPI

from .views.matches_view import match_view
from .views.slips_view import slip_view

app = FastAPI(title="BET CONVERTER")


app.include_router(match_view,prefix="/api/v1/resources",tags=["Matches"])
app.include_router(slip_view,prefix="/api/v1/resources",tags=["Slips"])
