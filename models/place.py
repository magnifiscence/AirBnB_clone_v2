#!/usr/bin/python3
""" Place Module for HBNB project that inherit the baseModel and Base"""
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, ForeignKey, String, Integer, Float, Table
from sqlalchemy.orm import relationship
import os
from models.amenity import Amenity


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place that is identified by many attributes """
    __tablename__ = "places"
    city_id = (Column(String(60), ForeignKey('cities.id'), nullable=False))
    user_id = (Column(String(60), ForeignKey('users.id'), nullable=False))
    name = (Column(String(128), nullable=False))
    description = (Column(String(1024), nullable=True))
    number_rooms = (Column(Integer, default=0, nullable=False))
    number_bathrooms = (Column(Integer, default=0, nullable=False))
    max_guest = (Column(Integer, default=0, nullable=False))
    price_by_night = (Column(Integer, default=0, nullable=False))
    latitude = (Column(Float, nullable=True))
    longitude = (Column(Float, nullable=True))
    # reviews = (relationship("Review", backref="place", cascade="delete"))
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship('Review', cascade='all, delete, delete-orphan',
                               backref='place')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False,
                                 back_populates='place_amenities')
    else:
        @property
        def reviews(self):
            from models import storage
            review_instances = storage.all("Review").values()
            return [review for review in review_instances
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """
            returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place
            """
            from models import storage
            amenity_instances = storage.all("Amenity").values()
            return [amenity for amenity in amenity_instances
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter attribute amenities that handles append method
            for adding an Amenity.id to the attribute amenity_ids.
            """
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
