from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
from sqlalchemy import create_engine

app = FastAPI()

plots_path = "/app/reports/plots"
if not os.path.exists(plots_path):
    os.makedirs(plots_path)
app.mount("/plots", StaticFiles(directory=plots_path), name="plots")

templates = Jinja2Templates(directory="templates")


def get_db_engine():
    return create_engine(
        f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    engine = get_db_engine()

    raw_data = pd.read_sql("SELECT * FROM raw_data LIMIT 10", con=engine).to_html(classes='table table-striped',
                                                                                  index=False)
    research_results = pd.read_sql("SELECT * FROM research_results", con=engine).to_html(classes='table table-hover',
                                                                                         index=False)
    plots = [f for f in os.listdir(plots_path) if f.endswith('.png')]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "raw_data": raw_data,
            "research": research_results,   
            "plots": plots
        }
    )