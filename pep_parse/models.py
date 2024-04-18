from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr

Base = declarative_base()


class Pep(Base):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    name = Column(String(200))
    status = Column(String(20))

    def __repr__(self):
        return f'{self.number} {self.name} ({self.status})'


class Statistic(Base):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    status = Column(String(20))
    status_count = Column(Integer)

    def __repr__(self):
        return f'{self.status} - {self.status_count}'
