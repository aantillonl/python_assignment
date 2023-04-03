import datetime
import statistics
from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from fastapi_pagination import Page, Params, paginate, add_pagination

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ctw_assignment import get_db_conn
from ctw_assignment.model import FinancialData

app = FastAPI()
add_pagination(app)
engine = get_db_conn()

@app.get("/api/financial_data")
async def get_financial_data(
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None,
    symbol: Optional[str] = None,
    params: Params = Depends()
):
    with Session(engine) as db_session:
        
        query = db_session.query(FinancialData)
        if start_date:
            query = query.filter(FinancialData.date >= start_date)
        if end_date:
            query = query.filter(FinancialData.date <= end_date)
        if symbol:
            query = query.filter(FinancialData.symbol == symbol)
        try:
            results = query.order_by(FinancialData.date).all()
        except SQLAlchemyError as ex:
            results = {"info": str(ex)}
        finally:
            json_compatible_item_data = jsonable_encoder(paginate(results, params))
            return JSONResponse(content=json_compatible_item_data)

@app.get("/api/statistics")
async def get_financial_data(
    start_date: datetime.date,
    end_date: datetime.date,
    symbol: str = None
):
    with Session(engine) as db_session:
        
        query = db_session.query(FinancialData) \
            .filter(FinancialData.date >= start_date) \
            .filter(FinancialData.date <= end_date) \
            .filter(FinancialData.symbol == symbol)
        results = {}
        try:
            results_raw = query.order_by(FinancialData.date).all()
            
        except SQLAlchemyError as ex:
            results["info"] = str(ex)
        else:
            average_daily_open_price = statistics.mean([r.open_price for r in results_raw])
            average_daily_close_price = statistics.mean([r.close_price for r in results_raw])
            average_daily_volume = statistics.mean([r.volume for r in results_raw])
            results["average_daily_open_price"] = average_daily_open_price,
            results["average_daily_close_price"] = average_daily_close_price,
            results["average_daily_volume"] = average_daily_volume
        finally:        
            json_compatible_item_data = jsonable_encoder(results)
            return JSONResponse(content=json_compatible_item_data)

