#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship



place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60), ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False, back_populates="place_amenities")

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
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

        @property
        def reviews(self):
            """returns the list of Review instances with place_id
            equals current Place.id"""
            reviews_list = []
            for k, v in storage.all(Review).items:
                if v.place_id == Place.id:
                    reviews_list.append(v)
            return reviews_list

        @property
        def amenities(self):
            amenities_list = []
            for k, v in storage.all(Amenity).items:
                if v.place_id == Place.id:
                    amenities_list.append(v)
            return amenities_list

        @amenities.setter
        def amenities(self, amenity=None):
            """adds Amenity.id to amenity_ids"""
            if amenity is not None:
                for k, v in storage.all(Amenity).items:
                    if v.place_id == Place.id:
                        amenity_ids.append(v)
