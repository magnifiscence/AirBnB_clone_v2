#!/usr/bin/python3
""" Review module for the HBNB project that inherit from basemodel and base """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Review class to store review information using different params """
    __tablename__ = "reviews"
    place_id = (Column(String(60), ForeignKey("places.id"), nullable=False))
    user_id = (Column(String(60), ForeignKey("users.id"), nullable=False))
    text = (Column(String(1024), nullable=False))

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
