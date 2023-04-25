from db import db
from sqlalchemy.sql import text
import users

def get_my_reviews(user_id):
    sql = text("""SELECT id, comment FROM reviews WHERE user_id=:user_id ORDER BY id""")
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def remove_review(review_id, user_id):
    sql = text("DELETE FROM reviews WHERE id=:review_id AND user_id=:user_id")
    db.session.execute(sql, {"review_id":review_id, "user_id":user_id})
    db.session.commit()
