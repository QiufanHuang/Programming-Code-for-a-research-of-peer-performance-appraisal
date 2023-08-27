import PPA_Game as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        yield Before_game, dict(player_nickname="xyz", player_comments="xyz")
        yield Beginning, dict(question_set=1)
        yield Task, dict(answer_1=5, answer_2=1, answer_3=5, answer_4=5, answer_5=2)
        yield Appraisal, dict(rate=10)
        yield Survey_after, dict(
            trusted=10,
            trust=0,
            cooperation=10,
            will_cooperate=10,
            rate_next=10,
            satisfaction=10,
        )
        yield Finish