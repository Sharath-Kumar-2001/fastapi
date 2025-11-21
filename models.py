from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class JobBoard(Base):
  __tablename__ = 'job_boards'
  id = Column(Integer, primary_key=True)
  slug = Column(String, nullable=False, unique=True)


class JobPost(Base):
  __tablename__ = 'job_posts'
  id = Column(Integer, primary_key=True)
  job_title = Column(String, nullable=False, unique=True)
  job_description = Column(String, nullable=False, unique=True)
  job_board_id = Column(Integer, ForeignKey("job_boards.id"), nullable=False)