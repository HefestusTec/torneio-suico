from database.models import Contestant, Tournament, Match


class DatabaseHandler:
    def __init__(self):
        pass

    def create_tournament(name):
        return Tournament.create(name=name)

    def set_tournament_rounds(tournament, rounds):
        tournament.rounds = rounds
        tournament.save()

    def go_to_next_round(tournament):
        tournament.current_round += 1
        tournament.save()

    def create_match(tournament, contestant1, contestant2, round):
        return Match.create(
            contestant1=contestant1,
            contestant2=contestant2,
            round=round,
            tournament=tournament,
        )

    def set_match_result(match, contestant1_score, contestant2_score):
        match.winner = (
            match.contestant1
            if contestant1_score > contestant2_score
            else match.contestant2
        )
        match.contestant1_score = contestant1_score
        match.contestant2_score = contestant2_score
        match.save()
