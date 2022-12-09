#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship, backref
import os

HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')


place_amenity = Table(
                    "place_amenity", Base.metadata,
                    Column(
                        "place_id", String(60), ForeignKey("places.id"),
                        primary_key=True, nullable=False
                        ), Column(
                        "amenity_id", String(60), ForeignKey("amenities.id"),
                        primary_key=True, nullable=False
                        )
                    )


class Place(BaseModel, Base if HBNB_TYPE_STORAGE == 'db' else object):
    """ A place to stay """
    if HBNB_TYPE_STORAGE == 'db':
        __tablename__ = 'places'
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            'Review', cascade="all,delete",
            backref=backref("place", cascade="all,delete"),
            passive_deletes=True,
            single_parent=True
            )
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False,
            back_populates="place_amenities"
        )

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    if HBNB_TYPE_STORAGE != 'db':
        @property
        def reviews(self):
            from models import storage
            from models.review import Review
            ls = []
            objects_cities = storage.all(Review)
            for review in objects_cities.values():
                if Review.place_id == self.id:
                    ls.append(review)
            return ls

        @property
        def amenities(self):
            from models import storage
            from models.amenity import Amenity
            ls = []
            objects_cities = storage.all(Amenity)
            for amenity in objects_cities.values():
                if Amenity.place_id == self.id:
                    ls.append(amenity)
            return ls
