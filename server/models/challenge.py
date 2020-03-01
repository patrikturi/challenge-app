from sqlalchemy import Column, Integer, String, BigInteger, Date

from server.models.abstractbase import AbstractBase
from server.models.calories import Calories
from server.utils.repository_util import RepositoryUtil


class Challenge(AbstractBase):
    __tablename__ = 'challenges'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo_util = RepositoryUtil(self.session)

    id = Column(Integer, primary_key=True)
    endomondo_id = Column(BigInteger, nullable=False, index=True, unique=True)

    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    def get_calories(self):
        all_calories = self.session.query(Calories).filter_by(challenge_id=self.id).all()
        return {calories.competitor_id: calories.kcal for calories in all_calories}

    def update(self, challenge_page):
        self.name = challenge_page.title
        self.start_date = challenge_page.start_date
        self.end_date = challenge_page.end_date
        self.session.commit()

        # TODO: already exists?
        self.repo_util.save_all(challenge_page.competitors)
        self.repo_util.save_calories(self.id, challenge_page)
