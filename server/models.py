from sqlalchemy import Column, Integer, String, BigInteger, Date
from server.database import Base


class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True)
    endomondo_id = Column(BigInteger, nullable=False, index=True, unique=True)

    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    def __repr__(self):
        return f'<Challenge(id={self.id}, endomondo_id={self.endomondo_id}, name={self.name})>'


class Competitor(Base):
    __tablename__ = 'competitors'

    id = Column(Integer, primary_key=True)
    endomondo_id = Column(BigInteger, nullable=False, index=True, unique=True)
    name = Column(String)
    calories = Column(Integer)

    display_name = Column(String)

    def __repr__(self):
        return f'<Competitor(id={id}, endomondo_id={self.endomondo_id}, name={self.name},' \
               f'displayName={self.display_name}, calories={self.calories})>'
