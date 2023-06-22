#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        name = ""

        @property
        def cities(self):
            """provides the filestorage relationship between
            cities and states"""
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == State.id:
                    city_list.append(city)
            return city_list
