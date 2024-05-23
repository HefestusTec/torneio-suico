import pickle

from swiss.match_log import MatchLog
from swiss.pairing_strategies import min_cost


class SwissHandler:
    def __init__(self) -> None:
        self.match_log = MatchLog()
        self.pairing_strategy = min_cost
        self.pairings = None
        self.__round = 0

    def add_contestants(self, contestants: list) -> None:
        self.contestants = contestants
        for contestant in contestants:
            self.match_log.add_player(contestant)

    def get_round_pairings(self, round: int) -> list:
        if round != self.__round:
            self.__round = round
            self.pairings = self.pairing_strategy.pairings(self.match_log)
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

    def save_state(self, file_path: str) -> None:
        match_log_path = file_path.replace(".pickle", "_match_log.pickle")
        with open(match_log_path, "wb") as file:
            pickle.dump(self.match_log, file)
        pairings_path = file_path.replace(".pickle", "_pairings.pickle")
        with open(pairings_path, "wb") as file:
            pickle.dump(self.pairings, file)

    def load_state(self, file_path: str) -> None:
        match_log_path = file_path.replace(".pickle", "_match_log.pickle")
        with open(match_log_path, "rb") as file:
            self.match_log = pickle.load(file)
        pairings_path = file_path.replace(".pickle", "_pairings.pickle")
        with open(pairings_path, "rb") as file:
            self.pairings = pickle.load(file)
