from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    UniqueConstraint
)

from dyeus.db import Base


class Appliance(Base):
    __tablename__ = 'appliance'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), unique=True)


class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    appliance = Column(Integer, ForeignKey('appliance.id'))
    name = Column(String(length=255))

    __table_args__ = (UniqueConstraint('appliance', 'name',
                                       name='_appliance_sensor_name_uc'),)


class SensorReading(Base):
    __tablename__ = 'sensor_reading'
    id = Column(Integer, primary_key=True)
    appliance = Column(Integer, ForeignKey('appliance.id'))
    timestamp = Column(DateTime(timezone=True))


class SensorValue(Base):
    __tablename__ = 'sensor_value'
    id = Column(Integer, primary_key=True)
    sensor_reading = Column(Integer, ForeignKey('sensor_reading.id'))
    sensor = Column(Integer, ForeignKey('sensor.id'))
    value = Column(String(length=31))
