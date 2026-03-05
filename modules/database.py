from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("sqlite:///data/company.db")

def run_query(query, params=None):
    with engine.connect() as conn:
        result = pd.read_sql(text(query), conn, params=params)
    return result