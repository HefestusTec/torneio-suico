from Swiss.match_log import MatchLog
from Swiss.pairing_strategies import min_cost


class SwissHandler:
    def __init__(self) -> None:
        self.match_log = MatchLog()
        self.pairing_strategy = min_cost
        self.pairings = None

    def add_contestants(self, contestants: list) -> None:
        self.contestants = contestants
        for contestant in contestants:
            self.match_log.add_player(contestant)

    def get_round_pairings(self) -> list:
        self.pairings = self.pairing_strategy.pairings(self.match_log)
        print(self.pairings.string())
        return self.pairings.pairs

    def get_bye_contestant(self) -> str:
        return self.pairings.bye_player

    def add_round_results(self, results: list) -> None:
        for result in results:
            contestant_a, contestant_b, score_a, score_b = result
            if contestant_b is None:
                self.match_log.add_bye(contestant_a, score_a)
            self.match_log.add_result(contestant_a, contestant_b, score_a, score_b)

    def add_bye_result(self, contestant: str, score: int) -> None:
        self.match_log.add_bye(contestant, score)

    def get_scoreboard(self) -> list:
        scoreboard = [
            (i + 1, contestant, self.match_log.player_score(contestant))
            for i, contestant in enumerate(self.match_log.ranking()[:-1])
        ]
        return scoreboard
