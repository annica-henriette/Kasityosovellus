from db import db
from sqlalchemy.sql import text
import users, instructions

def get_projects():
    sql = text("SELECT U.username, P.name, P.start_date, P.finishing_date, P.id FROM projects P, users U WHERE P.creator_id=U.id ORDER BY P.id")
    result = db.session.execute(sql)
    return result.fetchall()

def get_my_projects(user_id):
    sql = text("""SELECT id, name FROM projects
	       WHERE creator_id=:user_id ORDER BY name""")
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def get_project_info(project_id):
    sql = text("""SELECT p.name, p.material, p.start_date, p.finishing_date, u.username FROM projects p, users u
                  WHERE p.id=:project_id AND p.creator_id=u.id""")
    return db.session.execute(sql, {"project_id": project_id}).fetchone()

def get_project_instruction(project_id):
    sql = text("""SELECT i.id, i.name FROM projects p, instructions i WHERE p.id=:project_id AND p.instruction_used=i.id""")
    return db.session.execute(sql, {"project_id": project_id}).fetchone()

def add_project(creator_id, name, material, start_date, finishing_date, instruction_used):
    sql = text("""INSERT INTO projects (creator_id, name, material, start_date, finishing_date, instruction_used)
                  VALUES (:creator_id, :name, :material, :start_date, :finishing_date, :instruction_used)
                  RETURNING id""")
    project_id = db.session.execute(sql, {"creator_id":creator_id, "name":name, "material":material, "start_date":start_date, "finishing_date":finishing_date, "instruction_used":instruction_used}).fetchone()[0]
    db.session.commit()
    return project_id

def remove_project(project_id, user_id):
    sql = text("DELETE FROM projects WHERE id=:id AND creator_id=:user_id")
    db.session.execute(sql, {"id":project_id, "user_id":user_id})
    db.session.commit()

def add_review(project_id, user_id, stars, comment):
    sql = text("""INSERT INTO reviews (project_id, user_id, stars, comment)
	          VALUES (:project_id, :user_id, :stars, :comment)""")
    db.session.execute(sql, {"project_id":project_id, "user_id":user_id,
			     "stars":stars, "comment":comment})
    db.session.commit()

def get_review(project_id):
    sql = text("""SELECT u.username, r.stars, r.comment FROM reviews r, users u
	       WHERE r.user_id=u.id AND r.project_id=:project_id ORDER BY r.id""")
    return db.session.execute(sql, {"project_id":project_id}).fetchall()
