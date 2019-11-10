from server.utils.query_util import QueryUtil
from tests.unittests.dbtest_base import DbTestBase


class QueryUtilTests(DbTestBase):

    def setUp(self):
        super().setUp()
        self.query_util = QueryUtil(self.session)

    def test_getActiveChallenges_returnsChallengesRunningOrWithoutDate(self):

        all_active = self.query_util.get_active_challenges(self.current_date)

        self.assertEqual(4, len(all_active))
        self.assertEqual(self.challenge_running1.endomondo_id, all_active[0].endomondo_id)
        self.assertEqual(self.challenge_running2.endomondo_id, all_active[1].endomondo_id)
        self.assertEqual(self.challenge_without_date.endomondo_id, all_active[2].endomondo_id)

    def test_getInactiveChallenges_returnsChallengesStoppedOrNotStarted(self):

        all_inactive = self.query_util.get_inactive_challenges(self.current_date)

        self.assertEqual(2, len(all_inactive))
        self.assertEqual(self.challenge_ended.endomondo_id, all_inactive[0].endomondo_id)
        self.assertEqual(self.challenge_not_started.endomondo_id, all_inactive[1].endomondo_id)
