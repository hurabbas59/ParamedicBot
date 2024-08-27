# from sqlalchemy import Column, String, ForeignKey, JSON
# from sqlalchemy.dialects.postgresql import UUID
# from src.database.db_utils import Base
# from sqlalchemy.orm import relationship
# class User(Base):
#     __tablename__ = 'user'

#     user_id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
#     user_name = Column(String, index=True, nullable=False)
#     email = Column(String, index=True, unique=True, nullable=False)
#     password = Column(String, nullable=False)

# class ChatHistory(Base):
#     __tablename__ = 'chat_history'

#     chat_id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
#     user_id = Column(String, ForeignKey('user.user_id'), index=True, nullable=False)
#     chat_hist = Column(JSON, nullable=False)

#     user = relationship('User', back_populates='chats')

# class Subscription(Base):
#     __tablename__ = 'subscription'

#     sub_id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
#     user_id = Column(String, ForeignKey('user.user_id'), index=True, nullable=False)
#     license_level = Column(String, nullable=False)
#     sub_plan = Column(String, nullable=False)

#     user = relationship('User', back_populates='subscription')
    