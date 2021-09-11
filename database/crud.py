import config
from database.database import SessionLocal
from database.models import User, Post


def create_user(user_id: int) -> User:
    session = SessionLocal()
    db_user = User(telegram_id=user_id)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(user_id: int) -> User:
    session = SessionLocal()
    return session.query(User).filter(User.telegram_id == user_id).first()


def create_post(post_type: str, file_id: str, username: str = None) -> Post:
    session = SessionLocal()
    db_post = Post(
        post_type=post_type, file_id=file_id, username=username, post_status=config.PostStatuses.PENDING)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


def get_post(post_id: int) -> Post:
    session = SessionLocal()
    return session.query(Post).filter(Post.id == post_id).first()


def edit_post_type(post_id: int, post_status: int):
    session = SessionLocal()
    post = session.query(Post).filter_by(id=post_id)
    post.update({"post_status": post_status})
    session.commit()
