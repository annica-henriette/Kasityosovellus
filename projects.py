from db import db
from sqlalchemy.sql import text

def add_project(creator_id, name, material, start_date, finishin_date):
    sql = text("""INSERT INTO projects (creator_id, name, material, start_date, finishing_date)
                  VALUES (:creator_id, :name, :material, :start_date, :finishing_date)
                  RETURNING id""")
    project_id = db.session.execute(sql, {"creator_id":creator_id}).fetchone()[0]
    db.session.commit()
    return project_id
