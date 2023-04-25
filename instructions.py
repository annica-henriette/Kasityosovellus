from db import db
from sqlalchemy.sql import text
import users

def get_instructions():
    sql = text("""SELECT U.username, I.name, I.content, I.difficulty, I.id FROM instructions I, users U 
               WHERE I.creator_id=U.id ORDER BY I.id""")
    result = db.session.execute(sql)
    return result.fetchall()

def get_my_instructions(user_id):
    sql = text("""SELECT id, name, content, difficulty FROM instructions
	       WHERE creator_id=:user_id ORDER BY name""")
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def get_instruction_info(instruction_id):
    sql = text("""SELECT i.name, i.content, i.difficulty, u.username FROM instructions i, users u
                  WHERE i.id=:instruction_id AND i.creator_id=u.id""")
    return db.session.execute(sql, {"instruction_id": instruction_id}).fetchone()

def add_instruction(creator_id, name, content,difficulty):
    sql = text("""INSERT INTO instructions (creator_id, name, content, difficulty)
                  VALUES (:creator_id, :name, :content, :difficulty)
                  RETURNING id""")
    instruction_id = db.session.execute(sql, {"creator_id":creator_id, "name":name, "content":content, "difficulty":difficulty}).fetchone()[0]
    db.session.commit()
    return instruction_id

def remove_instruction(instruction_id, user_id):
    sql = text("DELETE FROM instructions WHERE id=:id AND creator_id=:user_id")
    db.session.execute(sql, {"id":instruction_id, "user_id":user_id})
    db.session.commit()

def add_review(instruction_id, user_id, stars, comment):
    sql = text("""INSERT INTO reviews (instruction_id, user_id, stars, comment)
	          VALUES (:instruction_id, :user_id, :stars, :comment)""")
    db.session.execute(sql, {"instruction_id":instruction_id, "user_id":user_id,
			     "stars":stars, "comment":comment})
    db.session.commit()

def get_review(instruction_id):
    sql = text("""SELECT u.username, r.stars, r.comment FROM reviews r, users u
	       WHERE r.user_id=u.id AND r.instruction_id=:instruction_id ORDER BY r.id""")
    return db.session.execute(sql, {"instruction_id":instruction_id}).fetchall()
