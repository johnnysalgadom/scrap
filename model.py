import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, String, Text, JSON

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = "Kajabi_Product"

    id = Column(String(64), primary_key=True)
    title = Column(String(512), nullable=True)
    description = Column(String(1024), nullable=True)
    thumbnail = Column(String(1024), nullable=True)
    json_data = Column(JSON, nullable=True)
    created_by = Column(String(64), nullable=True)
    created = Column(DateTime, default=datetime.datetime.now, nullable=False)


class CategoryModel(Base):
    __tablename__ = "Kajabi_Category"

    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), nullable=False)
    title = Column(String(512), nullable=True)
    description = Column(String(1024), nullable=True)
    poster_image = Column(String(1024), nullable=True)
    json_data = Column(JSON, nullable=True)
    created_by = Column(String(64), nullable=True)
    created = Column(DateTime, default=datetime.datetime.now, nullable=False)


class PostModel(Base):
    __tablename__ = "Kajabi_Post"

    id = Column(String(64), primary_key=True)
    category_id = Column(String(64), nullable=False)
    title = Column(String(512), nullable=True)
    publishing_status = Column(String(32), nullable=True)
    body = Column(Text, nullable=True)
    poster_image = Column(String(1024), nullable=True)
    json_data = Column(JSON, nullable=True)
    created_by = Column(String(64), nullable=True)
    created = Column(DateTime, default=datetime.datetime.now, nullable=False)

