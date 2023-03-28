from db import db
from sqlalchemy.sql import text
import users

def get_projects():
    sql = text("SELECT U.username, P.name, P.start_date, P.finishing_date  FROM projects P, users U WHERE P.creator_id=U.id ORDER BY P.id")
    result = db.session.execute(sql)
    return result.fetchall()

def get_project_info(project_id):
    sql = text("""SELECT p.name, p.material, p.start_date, p.finishing_date FROM projects p, users u
                  WHERE p.id=:project_id AND p.creator_id=u.id""")
    return db.session.execute(sql, {"project_id": project_id}).fetchone()

def add_project(creator_id, name, material, start_date, finishing_date):
    sql = text("""INSERT INTO projects (creator_id, name, material, start_date, finishing_date)
                  VALUES (:creator_id, :name, :material, :start_date, :finishing_date)
                  RETURNING id""")
    project_id = db.session.execute(sql, {"creator_id":creator_id, "name":name, "material":material, "start_date":start_date, "finishing_date":finishing_date}).fetchone()[0]
    db.session.commit()
    return project_id
