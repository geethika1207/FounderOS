from sqlalchemy import Column, String, INTEGER, ForeignKey, JSON
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class USER(Base):
    __tablename__ = "Users"

    id = Column(INTEGER, primary_key = True)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))

class blueprints(Base):
    __tablename__ = "analysis"

    id = Column(INTEGER, primary_key = True)
    user_id = Column(INTEGER, ForeignKey("Users.id", ondelete = "CASCADE"), nullable = False)  
    developer_idea = Column(String, unique = False, nullable = False)
    app_type = Column(JSON, nullable = False, unique = False)
    core_features = Column(JSON, nullable = False, unique = False)
    target_users = Column(JSON, nullable = False, unique = False)
    db_design = Column(JSON, nullable = False, unique = False)
    end_points = Column(JSON, nullable = False, unique = False)
    risk_factors = Column(JSON, nullable = False, unique = False)
    roadmap = Column(JSON, nullable = False, unique = False)

 
