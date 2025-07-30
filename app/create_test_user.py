from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

def create_user():
    username = "admin"
    password = "P@ssword124"
    hashed_pw = pwd_context.hash(password)

    user = User(username=username, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.close()
    print("Test user created.")

if __name__ == "__main__":
    create_user()
