from flask_sqlalchemy import Column, Integer, String, Float, Text, DateTime
from .db import Base


class Worker(Base):
    """Create Worker Model."""
    __tablename__ = 'jira'
    key = Column(String(20), primary_key=True)
    assignee = Column(String(50), unique=False, nullable=False)
    summary = Column(String(100), unique=False, nullable=False)
    status = Column(String(50), unique=False, nullable=False)
    priority = Column(String(50), unique=False, nullable=False)
    rank = Column(Integer, unique=False, nullable=False)
    issuetype = Column(Float, unique=False, nullable=False)
    epic_link = Column(String(50), unique=False)
    project = Column(String(50), unique=False)
    updated = Column(DateTime, unique=False)

    def __repr__(self):
        return '<Worker %r>' % self.title
