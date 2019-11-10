from sqlalchemy import or_, and_

from server.models.challenge import Challenge


class QueryUtil:

    def __init__(self, session):
        self.session = session

    def get_active_challenges(self, current_date):
        """
        NOTE:
         * having neither start_date and end_date happens when the challenge wasn't ever fetched/parsed yet
         * having only start date or end date is not a use case for this application
        """
        return self.session.query(Challenge).filter(
            or_(Challenge.start_date == None, Challenge.end_date == None,
                and_(Challenge.start_date <= current_date, Challenge.end_date >= current_date))).all()

    def get_inactive_challenges(self, current_date):
        return self.session.query(Challenge).filter(or_(
            Challenge.start_date > current_date, Challenge.end_date < current_date)).all()
