from sqlalchemy import Column, Integer, String, BigInteger

from server.models.abstractbase import AbstractBase


class Competitor(AbstractBase):
    __tablename__ = 'competitors'

    id = Column(Integer, primary_key=True)
    endomondo_id = Column(BigInteger, nullable=False, index=True, unique=True)
    name = Column(String)

    display_name = Column(String)

    def save(self):
        stored_competitor = self.session.query(Competitor).filter_by(endomondo_id=self.endomondo_id).first()

        if stored_competitor:
            self.id = stored_competitor.id
            self.session.merge(self)
        else:
            self.session.add(self)

        self.session.commit()
