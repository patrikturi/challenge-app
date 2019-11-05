from sqlalchemy import Column, Integer, String, BigInteger, Date

from server.models.abstractbase import AbstractBase


class Challenge(AbstractBase):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True)
    endomondo_id = Column(BigInteger, nullable=False, index=True, unique=True)

    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
