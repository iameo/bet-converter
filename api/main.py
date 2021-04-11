from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .views.matches_view import match_view
from .views.slips_view import slip_view

app = FastAPI(
    title="BET CONVERTER",
    description="API for converting a bet slip from one source to another!",
    version="alpha")


#Redirect to docs
@app.get("/", tags=['Docs'])
def docs():
    return RedirectResponse('/docs')

app.include_router(match_view,prefix="/api/v1/resources",tags=["Matches"])
app.include_router(slip_view,prefix="/api/v1/resources",tags=["Slips"])
