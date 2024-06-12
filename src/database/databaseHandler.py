from os import makedirs
from os.path import dirname, exists

from peewee import SqliteDatabase

from database.models import DB_PATH, Contestant, Match, Tournament


class DatabaseHandler:
    def __init__(self):
        if not exists(DB_PATH):
            makedirs(dirname(DB_PATH), exist_ok=True)
        self.__db = SqliteDatabase(DB_PATH)
        self.__db.connect()
        self.__db.create_tables([Contestant, Tournament, Match])
        # create relationship between Contestant and Tournament
        self.__db.create_tables([Contestant.tournaments.get_through_model()])

    def create_tournament(self, name):
        return Tournament.create(name=name)

    def get_tournaments(self):
        tournaments = [
            [tournament.id, tournament.name] for tournament in Tournament.select()
        ]
        return tournaments

    def get_tournament_by_id(self, tournament_id):
        return Tournament.get(Tournament.id == tournament_id)

    def get_tournament_contestants(self, tournament):
        return [contestant.name for contestant in tournament.contestants]

    def set_tournament_settings(self, tournament, rounds, max_round_score):
        tournament.rounds = rounds
        tournament.max_round_score = max_round_score
        tournament.save()

    def set_setup_stage(self, tournament, stage):
        tournament.setup_stage = stage
        tournament.save()

    def go_to_next_round(self, tournament):
        tournament.current_round += 1
        tournament.save()

    def create_contestant(self, name, tournament):
        new_contestant = Contestant.create(name=name)
        tournament.contestants.add(new_contestant)
        return new_contestant

    def delete_contestant(self, contestant_name, tournament):
        contestant_id = (
            tournament.contestants.where(Contestant.name == contestant_name).get().id
        )
        contestant = Contestant.get(Contestant.id == contestant_id)
        tournament.contestants.remove(contestant)
        contestant.delete_instance()

    def create_match(self, tournament, contestant1_name, contestant2_name, round):
        contestant1 = tournament.contestants.where(
            Contestant.name == contestant1_name
        ).get()
        contestant2 = (
            tournament.contestants.where(Contestant.name == contestant2_name).get()
            if contestant2_name
            else None
        )

        return Match.create(
            contestant1=contestant1,
            contestant2=contestant2,
            round=round,
            tournament=tournament,
        )

    def set_match_result(self, match, contestant1_score, contestant2_score):
        match.winner = (
            match.contestant1
            if contestant1_score > contestant2_score
            else match.contestant2
        )
        match.contestant1_score = contestant1_score
        match.contestant2_score = contestant2_score
        match.save()

    def get_matches_by_round(self, tournament, round):
        try:
            return tournament.matches.where(Match.round == round)
        except Exception:
            return []
