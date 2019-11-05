from sqlalchemy import Column, Integer, String, BigInteger

from server.models.abstractbase import AbstractBase


class Competitor(AbstractBase):
    __tablename__ = 'competitors'

    id = Column(Integer, primary_key=True)
    endomondo_id = Column(BigInteger, nullable=False, index=True, unique=True)
    name = Column(String)

    display_name = Column(String)
