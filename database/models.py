from sqlalchemy import Column, Integer, String

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    post_type = Column(String, nullable=False)
    file_id = Column(String, nullable=False)
    username = Column(String)
    post_status = Column(Integer, nullable=False)
