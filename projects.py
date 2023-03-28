from db import db
from sqlalchemy.sql import text
import users

def get_projects():
    sql = text("SELECT U.username, P.name, P.start_date, P.finishing_date  FROM projects P, users U WHERE P.creator_id=U.id ORDER BY P.id")
    result = db.session.execute(sql)
    return result.fetchall()

def add_project(creator_id, name, material, start_date, finishin_date):
    sql = text("""INSERT INTO projects (creator_id, name, material, start_date, finishing_date)
                  VALUES (:creator_id, :name, :material, :start_date, :finishing_date)
                  RETURNING id""")
    project_id = db.session.execute(sql, {"creator_id":creator_id}).fetchone()[0]
    db.session.commit()
    return project_id
