from db import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime

class Tcu(Base):
    __tablename__ = "tcu"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolean)
    latitude = Column(Float)
    longitude = Column(Float) 

    def get_attr_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "active": self.active,
            "latitude": self.latitude,
            "longitude": self.longitude
        }


class TcuData(Base):
    __tablename__ = "tcu_data"
    id = Column(Integer, primary_key=True)  
    tcu_id = Column(String) 
    datetime = Column(DateTime)
    tcu_datetime = Column(DateTime)
    status_id = Column(Integer)
    angular_position = Column(Float)
    target_angle = Column(Float)

    def get_attr_dict(self):
        return {
            "id": self.id,
            "tcu_id": self.tcu_id,
            "datetime": self.datetime.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "tcu_datetime": self.tcu_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "angular_position": self.angular_position,
            "target_angle": self.target_angle
        }
