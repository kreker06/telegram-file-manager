from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

base_name = 'file_manager.db'
engine = create_engine(f'sqlite:///{base_name}', echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String)

class Folder(Base):
    __tablename__ = "folder"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    folder_name = Column(String)
    parent_folder_id = Column(Integer, ForeignKey('folder.id'), nullable=True)

class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, index=True)
    folder_id = Column(Integer, ForeignKey('folder.id'), nullable=False)
    file_id = Column(String)
    tag = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)