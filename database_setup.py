import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'

    section = Column(String(20))
    itemtype = Column(String(20))
    description = Column(String(80), nullable = False)
    size = Column(Integer)
    brand = Column(String(20))
    image = Column(String(60))
    price = Column(String(8))
    rating = Column(Integer)
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):

        return {
            'id' : self.id,
            'description' : self.description,
            'price' : self.price,
            'image' : self.image,
            'section' : self.section,
            'itemtype' : self.itemtype,
            'size' : self.size,
            'brand' : self.brand,
            'rating' : self.rating,
    }


class User(Base):
    __tablename__ = 'users'

    name = Column(String(80), nullable = False)
    userid = Column(Integer, primary_key = True)

    @property
    def serialize(self):

        return {
            'name' : self.name,
            'userid' : self.userid,
    }

class Basketz(Base):
    __tablename__ = 'basketz'

    userid = Column(Integer)
    itemid = Column(Integer)
    qty = Column(Integer)
    basketid = Column(Integer, primary_key = True)

    @property
    def serialize(self):

        return {
            'userid' : self.userid,
            'itemid' : self.itemid,
            'qty' : self.qty,
            'basketid' : self.basketid,
        }
### Insert at end of file ###

engine = create_engine('sqlite:///productcatalog.db')

Base.metadata.create_all(engine)
