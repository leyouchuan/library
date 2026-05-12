from connect import SessionLocal
from sqlalchemy import text

with SessionLocal() as db:
    result = db.execute(text("SELECT 1"))
    print(result.fetchone())