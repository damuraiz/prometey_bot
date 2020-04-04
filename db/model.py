from db.user import User
from db.content import Content

from db.base import Session

if __name__ == '__main__':
    session = Session()

    users = session.query(User).all()
    for user in users:
        print(user.telegram_user_id)